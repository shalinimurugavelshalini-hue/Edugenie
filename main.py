from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="AI-powered educational assistant",
    version="1.0.0"
)


# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# -----------------------------
# Request Models
# -----------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class QnaRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


# -----------------------------
# Home Page
# -----------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
      request=request,
      name="index.html",
      context={
        "request": request
      }
)

# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Question & Answer
# -----------------------------

@app.post("/qa")
async def qa(payload: QnaRequest):

    answer = await answer_question(
        payload.question
    )

    return {
        "answer": answer
    }


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    answer = await explain_topic(
        payload.text
    )

    return {
        "answer": answer
    }


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    result = await generate_quiz(
        payload.text,
        payload.count
    )

    return result


# -----------------------------
# Summarization
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    summary = await summarize_text(
        payload.text
    )

    return {
        "summary": summary
    }


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: TextRequest
):

    path = await get_learning_recommendations(
        payload.text
    )

    return {
        "learning_path": path
    }