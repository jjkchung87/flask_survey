from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345fdshjfjkdshf'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def presentSurveyOptions():
    """presents survey options"""
    surveyNames= surveys.keys()
    if 'responses' not in session:
        session['responses'] = {}
        return render_template('home.html',surveys=surveyNames)
    else:
        return render_template('home.html',surveys=surveyNames)
    

@app.route('/', methods=['POST'])
def presentSurveyIntro():
    """"""
    selectedSurvey = request.form['selected-survey']
    if selectedSurvey in session['responses']:
        return redirect(f'/survey/{selectedSurvey}')
    else:
        session['responses'][selectedSurvey] = []
        return redirect(f'/survey/{selectedSurvey}')


@app.route('/survey/<survey>')
def presentSurveyInstructions(survey):
    
    title = surveys[survey].title
    instructions = surveys[survey].instructions
    return render_template('survey-start.html',title=title,instructions=instructions,survey=survey)


@app.route('/survey/<survey>/question/<int:number>')
def showQuestion(survey, number):
    
    if len(session['responses'][survey]) == len(surveys[survey].questions):
        return redirect(f'/survey/{survey}/thank-you')
    
    if number > len(session['responses'][survey]):
        flash('Have not completed earlier questions. Please complete questions in order.')
        return redirect(f"/survey/{survey}/question/{len(session['responses'][survey])}")
           
    else:
        questions = surveys[survey].questions
        q = questions[number].question
        choices = questions[number].choices
        allowText= questions[number].allow_text
        return render_template('questions.html',question=q,choices=choices,allowText=allowText)
        

@app.route('/survey/<survey>/question/<int:number>',methods=['POST'])
def handleResponse (survey, number):
    choice = request.form['selected_option']
    question = surveys[survey].questions[number].question

    if survey in session['responses']:
        responses = session['responses'][survey]
        responses.append(f'<b>{question}:</b> {choice}')
        session['responses'][survey] = responses
    else:
        session['responses'][survey] = [f'<b>{question}:</b> {choice}']


    if len(session['responses'][survey]) == len(surveys[survey].questions):
        return redirect('/thank-you')
    else:
        return redirect(f"/survey/{survey}/question/{len(session['responses'][survey])}")



@app.route('/<survey>/thank-you')
def showThankYou(survey):
    responses = session['responses'][survey]
    return render_template('thank-you.html',survey=survey,responses=responses)