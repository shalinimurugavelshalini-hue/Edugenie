from gemini_client import generate_content
from prompts import build_summary_prompt


async def summarize_text(text: str) -> str:
    """
    Create a concise study summary using Gemini.
    """

    if not text or not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    prompt = build_summary_prompt(
        text.strip()
    )

    summary = await generate_content(
        prompt
    )

    return summary