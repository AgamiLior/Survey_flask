from flask import Flask, request, render_template, redirect, flash, session
from random import randint, choice, sample
from surveys import satisfaction_survey as survey

from flask.json import jsonify
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
RESPONSES = "responses"

@app.route('/')
def show_survey():
    return render_template("home.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES] = []

    return redirect("/questions/0")


@app.route("/questions/<int:num>")
def show_question(num):
    """Display current question."""
    responses = session.get(RESPONSES)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {num}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]
    return render_template(
        "question.html", question_num=num, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")