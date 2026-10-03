import pytest

from prompts import (
    build_qa_prompt,
    build_explanation_prompt,
    build_quiz_prompt,
    build_summary_prompt,
    build_learning_path_prompt,
)


def test_qa_prompt():
    prompt = build_qa_prompt("What is DBMS?")

    assert "What is DBMS?" in prompt
    assert "EduGenie" in prompt


def test_explanation_prompt():
    prompt = build_explanation_prompt(
        "Operating System"
    )

    assert "Operating System" in prompt
    assert "simple" in prompt.lower()


def test_quiz_prompt():
    prompt = build_quiz_prompt(
        "Python is a programming language.",
        3
    )

    assert "Python" in prompt
    assert "3" in prompt


def test_summary_prompt():
    prompt = build_summary_prompt(
        "This is study material."
    )

    assert "study material" in prompt.lower()


def test_learning_path_prompt():
    prompt = build_learning_path_prompt(
        "Learn Python for AI"
    )

    assert "Learn Python for AI" in prompt
    assert "learning path" in prompt.lower()


@pytest.mark.asyncio
async def test_empty_question():
    from qna import answer_question

    with pytest.raises(ValueError):
        await answer_question("")


@pytest.mark.asyncio
async def test_empty_topic():
    from explanation_module import explain_topic

    with pytest.raises(ValueError):
        await explain_topic("")


@pytest.mark.asyncio
async def test_empty_summary():
    from summary_module import summarize_text

    with pytest.raises(ValueError):
        await summarize_text("")


@pytest.mark.asyncio
async def test_empty_learning_goal():
    from learning_path import get_learning_recommendations

    with pytest.raises(ValueError):
        await get_learning_recommendations("")