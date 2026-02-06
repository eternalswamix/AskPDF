def chunk_text(
    text: str,
    chunk_size: int | None = None,
    overlap: int | None = None,
    min_chunk: int = 900,
    max_chunk: int = 1800,
    max_chunks: int = 250
):
    """
    Adaptive chunking for unknown PDF sizes.

    - If chunk_size not given, auto choose based on text length
    - overlap defaults to 15% of chunk_size
    - prevents too many chunks (max_chunks)
    """

    if not text:
        return []

    total_len = len(text)

    # ✅ Auto chunk size by PDF text length
    if chunk_size is None:
        if total_len < 15_000:
            chunk_size = 1000
        elif total_len < 80_000:
            chunk_size = 1200
        elif total_len < 200_000:
            chunk_size = 1500
        else:
            chunk_size = 1800

    chunk_size = max(min_chunk, min(max_chunk, chunk_size))

    # ✅ Auto overlap
    if overlap is None:
        overlap = int(chunk_size * 0.15)

    overlap = max(120, min(overlap, int(chunk_size * 0.30)))

    chunks = []
    start = 0

    while start < total_len and len(chunks) < max_chunks:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks
