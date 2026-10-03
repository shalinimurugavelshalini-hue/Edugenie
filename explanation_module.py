from gemini_client import generate_content
from prompts import build_explanation_prompt


async def explain_topic(topic: str) -> str:
    """
    Explain a topic using simple, beginner-friendly language.
    """

    if not topic or not topic.strip():
        raise ValueError(
            "Topic cannot be empty."
        )

    prompt = build_explanation_prompt(
        topic.strip()
    )

    explanation = await generate_content(
        prompt
    )

    return explanation