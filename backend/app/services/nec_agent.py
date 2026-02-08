from app.services.openai_client import client

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
        model="gpt-5",
        input=f"{SYSTEM}\n\nQuestion:\n{question}",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            }
        },
    )

    return resp.output_text
