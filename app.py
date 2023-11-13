from flask import Flask, render_template, request, redirect, flash, session
from surveys import surveys
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY']='secret'

debug = DebugToolbarExtension(app)


@app.route('/')
def start_page():
    survey = surveys.get("satisfaction")
    return render_template('start.html', survey=survey)


@app.route('/thanks')
def thanks_page():
    raise
    return render_template('thanks.html')


@app.route('/reset-responses', methods=['POST'])
def reset_responses():
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_index>', methods = ['GET', 'POST'])
def question_page(question_index):
    survey = surveys.get("satisfaction")
    questions = survey.questions
    if question_index != len(session['responses']):
        question_index = len(session['responses'])
        flash('trying to access an invalid question')
        return redirect('/questions/' + str(question_index))
    if question_index >= len(questions):
        return redirect('/thanks')
    question = questions[question_index]
    if request.method == 'POST':
        answer = request.form['answer']
        responses = session['responses']
        responses.append(answer)
        session['responses'] = responses
        return redirect('/questions/' + str(question_index + 1))
    return render_template('question.html', question=question, question_index=question_index)



