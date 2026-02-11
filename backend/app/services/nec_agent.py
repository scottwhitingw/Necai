from openai import OpenAI

client = OpenAI()

SYSTEM = """
You are an NEC lookup assistant.

Rules:
- Use ONLY NEC text retrieved via file_search.
- If not found → say: Not found in NEC text provided.
- No speculation.

Output:
1) Answer
2) Conditions / Constraints
3) Citations
""".strip()


def nec_lookup(question: str, vector_store_id: str) -> str:
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        tools=[{"type": "file_search"}],
        tool_choice="auto",
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        },
    )

    # Most SDK versions expose output_text; keep a safe fallback.
    out = getattr(resp, "output_text", None)
    if out:
        return out

    # Fallback: try to extract any text blocks from output
    try:
        chunks = []
        for item in resp.output:
            if getattr(item, "type", "") == "message":
                for c in item.content:
                    if getattr(c, "type", "") == "output_text":
                        chunks.append(c.text)
        return "\n".join(chunks).strip()
    except Exception:
        return ""
