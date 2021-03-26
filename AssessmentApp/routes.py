from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from AssessmentApp import app
from AssessmentApp.models import *

@app.route('/')
def index():
    # testData = test.query.all()


    return render_template('index.html')#, test1 = testData)


@app.route('/addAss' , methods = ["GET", "POST"])
def addAss():
    if request.method == "POST":
        module_id = request.form['module']
        assessment_type = bool(request.form['assType'])
        assessment_name = request.form['assTitle']
        time_limit = datetime.strptime(request.form['assTime'], '%H:%M')
        start_date = datetime.strptime(request.form['assStart'] +" "+ request.form['assStartTime'], '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(request.form['assEnd'] +" "+ request.form['assEndTime'], '%Y-%m-%d %H:%M')
        release = datetime.strptime(request.form['assRel'] +" "+ request.form['assRelTime'], '%Y-%m-%d %H:%M')
        # assMarks = int(request.form['assMarks'])
        weighting = int(request.form['assWeight'])
        allowed_attemps = int(request.form['assAttemps'])
        assessment_instructions = request.form['assInstruc']




        # print(assType)
        ass = assessment_details(module_id = module_id, assessment_type = assessment_type, assessment_name = assessment_name, time_limit = time_limit, start_date = start_date, end_date = end_date, release = release, weighting = weighting, allowed_attemps = allowed_attemps,  assessment_instructions = assessment_instructions)
        db.session.add(ass)
        db.session.commit()


    return render_template('AssessmentDetails.html')

@app.route('/assessment/<int:id>', methods = ["GET", "POST"])
def Ass(id):

    ass = assessment_details.query.filter_by(id=id).first()


    questionIds = assessment_questions.query.filter_by(assessment_id=id).all()

    assQuestions = [ question.query.filter_by(id=q.question_id).first() for q in questionIds]

    if request.method == "POST":
        correct = 0
        totalPossibleMarks = 0
        for i, q in enumerate (assQuestions):#
            totalPossibleMarks += q.value
            if q.correct_answer and request.form['Q' +str(q.id)] == str(q.correct_answer):
                correct += q.value
            elif (not q.correct_answer) and request.form['Q' +str(q.id)] == str(q.type_2_answer):
                correct += q.value
        flash(str(correct) + "/" + str(totalPossibleMarks) + " Marks")



    return render_template('UndertakeAss.html',  assQuestions =assQuestions, ass = ass, id = id)


@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('Login successful!')
      return redirect(url_for('home'))
    flash('Invalid email address or password.')

    return render_template('login.html',form=form)

  return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('login'))
