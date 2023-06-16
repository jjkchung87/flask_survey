from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def presentAndStartSurvey():
    """presents and starts survey"""
    title = survey.title
    instructions = survey.instructions

    return render_template('home.html',title=title,instructions=instructions)


@app.route('/question/<int:number>')
def showQuestion(number):
    
    if number > len(responses):
        flash('Have not completed earlier questions. Please complete questions in order.')
        return redirect(f'/question/{len(responses)}')
        
 
    else:
        questions = survey.questions
        q = questions[number].question
        choices = questions[number].choices
        return render_template('questions.html',question=q,choices=choices)

@app.route('/question/<int:number>',methods=['POST'])
def handleResponse (number):
    choice = request.form['selected_option']
    responses.append(choice)
    if len(responses) == len(survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/question/{number+1}')



@app.route('/thank-you')
def showThankYou():
    return render_template('thank-you.html')