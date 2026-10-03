from gemini_client import generate_content
from prompts import build_learning_path_prompt


async def get_learning_recommendations(goal: str) -> str:
    """
    Generate a structured learning path based on
    the student's goal.
    """

    if not goal or not goal.strip():
        raise ValueError(
            "Learning goal cannot be empty."
        )

    prompt = build_learning_path_prompt(
        goal.strip()
    )

    learning_path = await generate_content(
        prompt
    )

    return learning_path