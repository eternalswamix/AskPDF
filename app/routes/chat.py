from flask import Blueprint, render_template, request, session
from app.core.decorators import login_required
from app.core.extensions import supabase

from app.services.chat.vector_store import search_in_vector_db
from app.services.chat.rag_pipeline import generate_answer
import logging

chat_bp = Blueprint("chat", __name__)
logger = logging.getLogger(__name__)

@chat_bp.route("/chat/<pdf_id>", methods=["GET", "POST"])
@login_required
def chat(pdf_id):
    user_id = session["user"]["id"]

    # ✅ Sidebar PDFs (show original name)
    pdf_list = supabase.table("pdf_files") \
        .select("id, filename, original_filename, created_at") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()

    pdfs = pdf_list.data if pdf_list.data else []

    # ✅ Load history
    chat_rows = supabase.table("chat_history") \
        .select("id, question, answer, created_at") \
        .eq("pdf_id", pdf_id) \
        .eq("user_id", user_id) \
        .order("created_at", desc=False) \
        .execute()

    messages = []
    if chat_rows.data:
        for row in chat_rows.data:
            messages.append({"q": row["question"], "a": row["answer"]})

    if request.method == "POST":
        question = (request.form.get("question") or "").strip()

        if not question:
            return render_template(
                "chat.html",
                user=session.get("user"),
                pdf_id=pdf_id,
                messages=messages,
                pdfs=pdfs,
                error="Please type a question."
            )

        q_lower = question.lower()

        try:
            # ✅ Summary
            if "summary" in q_lower or "summarize" in q_lower:
                context_results = search_in_vector_db(pdf_id, "overall document summary", top_k=10)

                if not context_results:
                    answer = "❌ Summary generate nahi ho paya, because PDF indexing incomplete hai. Please re-upload PDF."
                else:
                    context = "\n\n".join([r["text"] for r in context_results])

                    if "short" in q_lower:
                        summary_prompt = "Give a short summary of this PDF in 6-8 bullet points."
                    else:
                        summary_prompt = "Give a clean structured summary of this PDF in bullet points."

                    answer = generate_answer(summary_prompt, context)

            else:
                # ✅ Normal question
                results = search_in_vector_db(pdf_id, question, top_k=8)

                if not results:
                    answer = "❌ Is PDF me iska answer available nahi hai."
                else:
                    # ✅ similarity threshold (tuneable)
                    filtered = [r for r in results if r["similarity"] > 0.20]

                    if not filtered:
                        answer = "❌ Is PDF me iska answer available nahi hai."
                    else:
                        context = "\n\n".join([r["text"] for r in filtered])
                        answer = generate_answer(question, context)
                        
        except Exception as e:
            logger.error(f"Chat RAG/Generation failed: {e}", exc_info=True)
            answer = "❌ Sorry, I encountered an error while processing your request. Please try again."

        # ✅ Save chat history
        supabase.table("chat_history").insert({
            "pdf_id": pdf_id,
            "user_id": user_id,
            "question": question,
            "answer": answer
        }).execute()

        messages.append({"q": question, "a": answer})

    return render_template(
        "chat.html",
        user=session.get("user"),
        pdf_id=pdf_id,
        messages=messages,
        pdfs=pdfs
    )
