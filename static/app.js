// ===============================
// EduGenie Frontend JavaScript
// ===============================


// ===============================
// Feature Navigation
// ===============================

function showFeature(featureId) {

    const sections =
        document.querySelectorAll(".feature-section");

    const buttons =
        document.querySelectorAll(".tab-button");


    sections.forEach(section => {

        section.classList.remove("active");

    });


    buttons.forEach(button => {

        button.classList.remove("active");

    });


    const selectedSection =
        document.getElementById(featureId);

    if (selectedSection) {

        selectedSection.classList.add("active");

    }


    const selectedButton =
        document.querySelector(
            `.tab-button[onclick="showFeature('${featureId}')"]`
        );

    if (selectedButton) {

        selectedButton.classList.add("active");

    }
}


// ===============================
// Common API Request Function
// ===============================

async function sendRequest(
    endpoint,
    data
) {

    const response =
        await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });


    const contentType = response.headers.get("content-type") || "";

    let result;

    if (contentType.includes("application/json")) {
       result = await response.json();
    } else {
        const text = await response.text();
        result = {
           detail: text || "Server returned an invalid response."
    };
}


    if (!response.ok) {

        throw new Error(
            result.detail ||
            "Something went wrong."
        );

    }


    return result;
}


// ===============================
// Result Helpers
// ===============================

function showLoading(element) {

    element.classList.add("show");

    element.classList.remove("error");

    element.innerHTML =
        '<div class="loading">🤖 EduGenie is thinking...</div>';
}


function showError(
    element,
    message
) {

    element.classList.add("show");

    element.classList.add("error");

    element.textContent =
        "❌ " + message;
}


function showResult(
    element,
    content
) {

    element.classList.add("show");

    element.classList.remove("error");

    element.innerHTML = "";

    const output =
        document.createElement("div");

    output.textContent =
        content;

    element.appendChild(output);
}


// ===============================
// Ask Question
// ===============================

async function askQuestion() {

    const input =
        document.getElementById("qaInput");

    const result =
        document.getElementById("qaResult");


    const question =
        input.value.trim();


    if (!question) {

        showError(
            result,
            "Please enter a question."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await sendRequest(
                "/qa",
                {
                    question: question
                }
            );


        showResult(
            result,
            data.answer
        );


    } catch (error) {

        showError(
            result,
            error.message
        );

    }
}


// ===============================
// Explain Topic
// ===============================

async function explainTopic() {

    const input =
        document.getElementById(
            "explainInput"
        );

    const result =
        document.getElementById(
            "explainResult"
        );


    const topic =
        input.value.trim();


    if (!topic) {

        showError(
            result,
            "Please enter a topic."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await sendRequest(
                "/explain",
                {
                    text: topic
                }
            );


        showResult(
            result,
            data.answer
        );


    } catch (error) {

        showError(
            result,
            error.message
        );

    }
}


// ===============================
// Generate Quiz
// ===============================

async function generateQuiz() {

    const input =
        document.getElementById(
            "quizInput"
        );

    const countInput =
        document.getElementById(
            "quizCount"
        );

    const result =
        document.getElementById(
            "quizResult"
        );


    const text =
        input.value.trim();


    const count =
        Number(
            countInput.value
        );


    if (!text) {

        showError(
            result,
            "Please enter study material."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await sendRequest(
                "/quiz",
                {
                    text: text,
                    count: count
                }
            );


        displayQuiz(
            result,
            data
        );


    } catch (error) {

        showError(
            result,
            error.message
        );

    }
}


// ===============================
// Display Quiz
// ===============================

function displayQuiz(
    container,
    data
) {

    container.classList.add("show");

    container.classList.remove("error");

    container.innerHTML = "";


    if (
        data.format === "json" &&
        data.quiz
    ) {

        const quiz =
            data.quiz;


        const questions =
            Array.isArray(quiz)
                ? quiz
                : quiz.questions;


        if (
            Array.isArray(questions)
        ) {

            questions.forEach(
                (question, index) => {

                    const card =
                        document.createElement(
                            "div"
                        );

                    card.className =
                        "quiz-question";


                    const title =
                        document.createElement(
                            "h3"
                        );

                    title.textContent =
                        `${index + 1}. ${
                            question.question || ""
                        }`;


                    card.appendChild(title);


                    const options =
                        question.options ||
                        {};


                    Object.entries(
                        options
                    ).forEach(
                        ([key, value]) => {

                            const option =
                                document.createElement(
                                    "div"
                                );

                            option.className =
                                "quiz-option";

                            option.textContent =
                                `${key}. ${value}`;

                            card.appendChild(
                                option
                            );

                        }
                    );


                    if (
                        question.answer ||
                        question.correct_answer
                    ) {

                        const answer =
                            document.createElement(
                                "div"
                            );

                        answer.className =
                            "quiz-answer";

                        answer.textContent =
                            `Correct Answer: ${
                                question.answer ||
                                question.correct_answer
                            }`;


                        card.appendChild(
                            answer
                        );

                    }


                    if (
                        question.explanation
                    ) {

                        const explanation =
                            document.createElement(
                                "p"
                            );

                        explanation.style.marginTop =
                            "10px";

                        explanation.textContent =
                            `Explanation: ${
                                question.explanation
                            }`;


                        card.appendChild(
                            explanation
                        );

                    }


                    container.appendChild(
                        card
                    );

                }
            );


            return;

        }

    }


    // Fallback if Gemini returns plain text

    const fallback =
        document.createElement(
            "div"
        );

    fallback.textContent =
        data.quiz || "No quiz generated.";

    container.appendChild(
        fallback
    );
}


// ===============================
// Summarize Text
// ===============================

async function summarizeText() {

    const input =
        document.getElementById(
            "summaryInput"
        );

    const result =
        document.getElementById(
            "summaryResult"
        );


    const text =
        input.value.trim();


    if (!text) {

        showError(
            result,
            "Please enter text to summarize."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await sendRequest(
                "/summarize",
                {
                    text: text
                }
            );


        showResult(
            result,
            data.summary
        );


    } catch (error) {

        showError(
            result,
            error.message
        );

    }
}


// ===============================
// Learning Path
// ===============================

async function createLearningPath() {

    const input =
        document.getElementById(
            "learningInput"
        );

    const result =
        document.getElementById(
            "learningResult"
        );


    const goal =
        input.value.trim();


    if (!goal) {

        showError(
            result,
            "Please enter your learning goal."
        );

        return;
    }


    showLoading(result);


    try {

        const data =
            await sendRequest(
                "/learn/recommendations",
                {
                    text: goal
                }
            );


        showResult(
            result,
            data.learning_path
        );


    } catch (error) {

        showError(
            result,
            error.message
        );

    }
}


// ===============================
// Enter Key Support
// ===============================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const qaInput =
            document.getElementById(
                "qaInput"
            );


        if (qaInput) {

            qaInput.addEventListener(
                "keydown",
                event => {

                    if (
                        event.ctrlKey &&
                        event.key === "Enter"
                    ) {

                        askQuestion();

                    }

                }
            );

        }

    }
);