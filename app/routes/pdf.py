import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from app.core.decorators import login_required
from app.core.extensions import supabase

from app.services.chat.pdf_utils import extract_text_from_pdf_bytes
from app.services.chat.chunking import chunk_text
from app.services.chat.vector_store import add_to_vector_db
import logging

pdf_bp = Blueprint("pdf", __name__)
logger = logging.getLogger(__name__)

@pdf_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_pdf():
    if request.method == "POST":
        pdf_file = request.files.get("pdf")

        if not pdf_file:
            return render_template("upload.html", user=session.get("user"), error="Please upload a PDF file.")

        original_name = secure_filename(pdf_file.filename)
        if not original_name or not original_name.lower().endswith(".pdf"):
            return render_template("upload.html", user=session.get("user"), error="Only PDF files are allowed.")

        unique_name = f"{uuid.uuid4()}_{original_name}"
        user_id = session["user"]["id"]

        # ✅ Read bytes ONCE (works in Vercel)
        file_bytes = pdf_file.read()

        # ✅ Upload to Supabase Storage
        storage_path = f"{user_id}/{unique_name}"

        try:
            supabase.storage.from_("pdfs").upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": "application/pdf"}
            )
        except Exception as e:
            logger.error(f"Supabase Storage upload failed for {unique_name}: {e}", exc_info=True)
            return render_template(
                "upload.html",
                user=session.get("user"),
                error=f"Supabase Storage upload failed: {str(e)}"
            )

        # ✅ Save metadata in DB
        pdf_row = supabase.table("pdf_files").insert({
            "user_id": user_id,
            "filename": unique_name,
            "original_filename": original_name,
            "storage_path": storage_path
        }).execute()

        if not pdf_row.data:
            return render_template("upload.html", user=session.get("user"), error="PDF saved but DB insert failed.")

        pdf_id = pdf_row.data[0]["id"]

        # ✅ Extract text directly from bytes (NO LOCAL TEMP FILE)
        try:
            text = extract_text_from_pdf_bytes(file_bytes)

            # ✅ Adaptive chunking (your latest logic)
            chunks = chunk_text(text)

            # ✅ Store chunks into Supabase pgvector table
            add_to_vector_db(pdf_id, user_id, chunks)
            
        except Exception as e:
            logger.error(f"PDF Processing/Vector Store failed for {original_name}: {e}", exc_info=True)
            # Optional: Delete the file from DB/Storage to clean up?
            return render_template("upload.html", user=session.get("user"), error=f"Processing failed: {str(e)}")

        return redirect(url_for("chat.chat", pdf_id=pdf_id))

    return render_template("upload.html", user=session.get("user"))
