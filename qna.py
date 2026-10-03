from gemini_client import generate_content
from prompts import build_qa_prompt


async def answer_question(question: str) -> str:
    """
    Answer a student's question using Gemini.
    """

    if not question or not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    prompt = build_qa_prompt(
        question.strip()
    )

    answer = await generate_content(
        prompt
    )

    return answer