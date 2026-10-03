import json
import re

from gemini_client import generate_content
from prompts import build_quiz_prompt


def clean_json_response(text: str) -> str:
    """
    Remove markdown code fences from Gemini JSON response.
    """

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


async def generate_quiz(
    text: str,
    count: int = 3
) -> dict:
    """
    Generate the requested number of MCQ questions.
    """

    if not text or not text.strip():
        raise ValueError(
            "Study material cannot be empty."
        )

    if count < 1 or count > 10:
        raise ValueError(
            "Quiz count must be between 1 and 10."
        )

    prompt = build_quiz_prompt(
        text.strip(),
        count
    )

    response = await generate_content(
        prompt
    )

    cleaned_response = clean_json_response(
        response
    )

    try:
        quiz_data = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError:
        return {
            "quiz": response,
            "format": "text"
        }

    # ---------------------------------
    # Gemini returned a LIST
    # ---------------------------------

    if isinstance(quiz_data, list):

        questions = quiz_data

    # ---------------------------------
    # Gemini returned a DICTIONARY
    # ---------------------------------

    elif isinstance(quiz_data, dict):

        questions = quiz_data.get(
            "questions",
            []
        )

    else:

        questions = []

    # ---------------------------------
    # Make sure we have a list
    # ---------------------------------

    if not isinstance(questions, list):

        questions = []

    # ---------------------------------
    # Return requested number
    # ---------------------------------

    questions = questions[:count]

    return {
        "quiz": {
            "questions": questions
        },
        "format": "json"
    }