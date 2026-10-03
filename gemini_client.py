import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


def fallback_answer(prompt: str) -> str:
    """
    Local fallback responses used when Gemini API is unavailable.
    Detects the requested EduGenie feature from the prompt.
    """

    text = prompt.lower()

    # =========================================================
    # QUIZ
    # =========================================================
    if "multiple-choice questions" in text or "quiz generator" in text:

        material = "the given study material"

        if "operating system" in text:
            material = "Operating System"

        elif "artificial intelligence" in text or "artificial intelligence" in text:
            material = "Artificial Intelligence"

        elif "database" in text or "dbms" in text:
            material = "DBMS"

        quiz = [
            {
                "question": f"What is the main purpose of {material}?",
                "options": {
                    "A": "To perform useful computing tasks",
                    "B": "To only store images",
                    "C": "To only play games",
                    "D": "To turn off a computer"
                },
                "answer": "A",
                "explanation": f"{material} is used to perform useful computing-related tasks."
            },
            {
                "question": f"Which statement about {material} is correct?",
                "options": {
                    "A": "It has no practical use",
                    "B": "It helps solve computing problems",
                    "C": "It only works without computers",
                    "D": "It cannot be studied"
                },
                "answer": "B",
                "explanation": f"{material} is useful for solving computing problems."
            },
            {
                "question": f"Why should students learn {material}?",
                "options": {
                    "A": "To understand important computing concepts",
                    "B": "Only for entertainment",
                    "C": "To avoid using technology",
                    "D": "It has no applications"
                },
                "answer": "A",
                "explanation": f"Learning {material} helps students understand important computing concepts."
            }
        ]

        # Try to read requested count
        match = re.search(r"create\s+(\d+)\s+multiple", text)

        if match:
            count = int(match.group(1))
            count = max(1, min(count, 3))
            quiz = quiz[:count]

        return json.dumps(quiz, indent=2)


    # =========================================================
    # EXPLANATION
    # =========================================================
    if "explain the following topic" in text or "simple definition" in text:

        topic = "the requested topic"

        if "operating system" in text:
            topic = "Operating System"

        elif "artificial intelligence" in text:
            topic = "Artificial Intelligence"

        elif "database" in text or "dbms" in text:
            topic = "DBMS"

        elif "distributed computing" in text:
            topic = "Distributed Computing"

        return f"""
1. Simple Definition

{topic} is an important concept in computer science that helps computers
perform and manage different tasks.

2. Main Idea

The main idea is to understand what {topic} does and why it is useful.

3. How It Works

It works by using its main components or processes to perform the required
operations.

4. Important Points

• Understand its basic definition.
• Learn its main components.
• Understand how it works.
• Study its advantages and applications.

5. Simple Example

A real-world computer application can use {topic} to perform useful tasks.

6. Short Recap

In simple words, {topic} is a useful computer science concept that helps
us understand how computing systems work.
"""


    # =========================================================
    # SUMMARY
    # =========================================================
    if "summarize" in text or "quick revision notes" in text:

        return """
📚 QUICK SUMMARY

Overview:
The given text contains important information that can be studied by
identifying its main concepts and key points.

Important Concepts:
• Basic definition
• Main components
• Working process
• Important features
• Applications

Key Points:
1. Understand the basic concept.
2. Remember the important terms.
3. Understand how the process works.
4. Study important applications.
5. Revise the main points before the exam.

Important Terms:
• Definition
• Components
• Process
• Features
• Applications

📝 Quick Revision:
Learn the definition first, then understand the working, important
features, and real-world applications.
"""


    # =========================================================
    # LEARNING PATH
    # =========================================================
    if "learning path" in text or "learning-path advisor" in text:

        return """
🎯 LEARNING PATH

1. Goal
Understand the requested topic from beginner to advanced level.

2. Prerequisites
• Basic computer knowledge
• Basic programming concepts
• Logical thinking

3. Beginner Topics
• Basic definitions
• Fundamental concepts
• Important terminology
• Simple examples

4. Intermediate Topics
• Main components
• Working principles
• Practical examples
• Problem solving

5. Advanced Topics
• Advanced concepts
• Real-world applications
• Performance considerations
• Advanced problem solving

6. Practice Activities
• Solve basic questions
• Practice coding problems
• Create small examples
• Revise important concepts

7. Suggested Projects
• Build a small educational application
• Create a simple practical project
• Add a user interface

8. Final Skills
After completing this path, you should be able to explain the topic,
solve basic problems, and apply the concepts in a practical project.
"""


    # =========================================================
    # QUESTION & ANSWER
    # =========================================================

    if "student question" in text:

        if "artificial intelligence" in text or "what is ai" in text:
            return """
Artificial Intelligence (AI) is a branch of computer science that enables
machines to perform tasks that normally require human intelligence.

AI can learn from data, recognize patterns, understand language, solve
problems, and make decisions.

Examples:
• ChatGPT
• Voice assistants
• Recommendation systems
• Facial recognition

In simple words, AI makes computers capable of performing intelligent tasks.
"""

        if "operating system" in text or "what is os" in text:
            return """
An Operating System (OS) is system software that manages computer hardware
and software.

It acts as a connection between the user and the computer hardware.

Main functions:
• Process management
• Memory management
• File management
• Device management

Examples include Windows, Linux, macOS, Android, and iOS.

In simple words, the OS helps the computer and its applications work properly.
"""

        if "dbms" in text or "database" in text:
            return """
DBMS stands for Database Management System.

It is software used to store, organize, manage, and retrieve data.

Main functions:
• Insert data
• Update data
• Delete data
• Search data
• Provide security

Examples include MySQL, Oracle, PostgreSQL, and SQL Server.

In simple words, DBMS helps us manage data efficiently.
"""

        return """
EduGenie Answer

The question is related to an important computer science concept.

To understand it:
• Start with the basic definition.
• Learn its main components.
• Understand how it works.
• Study a simple example.
• Finally, learn its practical applications.

This gives a clear beginner-friendly understanding of the topic.
"""


    # =========================================================
    # GENERAL FALLBACK
    # =========================================================

    return """
EduGenie is currently using a local demo response because the Gemini API
is temporarily unavailable.

Please use the feature-specific sections above to study the topic.
"""


async def generate_content(prompt: str) -> str:
    """
    Generate content using Gemini.
    If Gemini is unavailable, use feature-specific local responses.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    # Try Gemini first
    if client:
        try:
            response = await client.aio.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            if response.text:
                return response.text

        except errors.ClientError:
            pass

        except errors.ServerError:
            pass

        except Exception:
            pass

    # Use local feature-specific fallback
    return fallback_answer(prompt)