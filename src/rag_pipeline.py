from src.gemini_client import generate_text

def generate_answer(question: str, context: str):
    prompt = f"""
You are a helpful PDF assistant.
Answer ONLY using the provided PDF context.

Rules:
- Do NOT use markdown formatting like **bold**, headings, code blocks.
- Write in clean plain text.
- If answer is not in context, reply exactly:
Is PDF me iska answer available nahi hai.

PDF Context:
{context}

User Question:
{question}

Answer:
"""
    return generate_text(prompt).strip()
