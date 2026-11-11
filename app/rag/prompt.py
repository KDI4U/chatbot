class PromptBuilder:

    @staticmethod
    def build(context: str, question: str):

        if context.strip():
            return f"""
You are BSWAN Smart Library Assistant.

Instructions:
- Use the provided context as the primary source.
- If the context is incomplete, you may use your general knowledge.
- If the question is unrelated to the context, answer using your general knowledge.
- Do not mention whether the answer came from documents.

Context:
{context}

Question:
{question}

Answer:
"""

        return f"""
You are BSWAN Smart Library Assistant.

Answer the following question using your own general knowledge.

Question:
{question}

Answer:
"""