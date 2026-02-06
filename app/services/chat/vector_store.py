from app.core.extensions import supabase
from app.services.chat.gemini_client import get_embedding

BATCH_SIZE = 60  # ✅ safe batch insert size


def add_to_vector_db(pdf_id: str, user_id: str, chunks: list[str], api_key=None):
    """
    Save chunks + embeddings into Supabase table: pdf_chunks
    Uses batch inserts to avoid payload size limits.
    """
    if not chunks:
        return

    rows = []
    for chunk in chunks:
        emb = get_embedding(chunk, api_key=api_key)

        rows.append({
            "pdf_id": pdf_id,
            "user_id": user_id,
            "content": chunk,
            "embedding": emb
        })

        # ✅ insert batch
        if len(rows) >= BATCH_SIZE:
            supabase.table("pdf_chunks").insert(rows).execute()
            rows = []

    # ✅ insert remaining
    if rows:
        supabase.table("pdf_chunks").insert(rows).execute()


def search_in_vector_db(pdf_id: str, query: str, top_k: int = 6, api_key=None):
    """
    Search using Supabase RPC function: match_pdf_chunks
    Returns: [{text, similarity}]
    """
    query_emb = get_embedding(query, api_key=api_key)

    res = supabase.rpc("match_pdf_chunks", {
        "query_embedding": query_emb,
        "match_pdf_id": pdf_id,
        "match_count": top_k
    }).execute()

    results = []
    if res.data:
        for row in res.data:
            results.append({
                "text": row["content"],
                "similarity": row["similarity"]
            })

    return results
