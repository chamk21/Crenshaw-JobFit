from app import app,db
from flask import render_template,flash,redirect, url_for,request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User,Set,quiz,Solution,Feedback,Tasks,Aptitude,AptAnswer,VerbReason,VerbReasonAnswer
from werkzeug.urls import url_parse
from app.forms import RegistrationForm,Quiz,VerbReasonform,EditProfileForm
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,admin=False,assessor=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_set',methods=['GET', 'POST'])
@login_required
def add_set():
    if current_user.username=='Admin':
        if request.method=='POST':
            set_name=request.form['name']
            set_about=request.form['about']
            new_set=Set(set_name=set_name,set_about=set_about)
            db.session.add(new_set)
            db.session.commit()
            return redirect(url_for('add_set'))
        else:
            all_sets=Set.query.all()
            return render_template('add_set.html',sets=all_sets)
    else:
        return render_template('accessdenied.html')
    
@app.route('/add_set/delete_set/<int:id>')
@login_required
def delete_set(id):
    get_set=Set.query.get_or_404(id)
    db.session.delete(get_set)
    db.session.commit()
    return redirect(url_for('add_set'))

@app.route('/add_set/edit_set/<int:id>',methods=['GET','POST'])
def edit_set(id):
    get_set=Set.query.get_or_404(id)
    if request.method=='POST':
        get_set.set_name=request.form['name']
        get_set.set_about=request.form['about']
        db.session.commit()
        return redirect(url_for('add_set'))
    else:
        return render_template('edit_set.html',setinfo=get_set)
    

@app.route('/add_set/add_questions_to_set/<int:id>',methods=['GET', 'POST'])
def add_questions_to_set(id):
    if request.method=='POST':
        problem_name=request.form['name']
        problem_timelimit=request.form['timelimit']
        setname=Set.query.get_or_404(id).set_name
        new_quiz=quiz(quiz_name = problem_name,setid = Set.query.get_or_404(id).id,time_limit=problem_timelimit,setname=setname)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('add_set'))
    else:
        return render_template('add_questions_to_set.html',specific_set=Set.query.get_or_404(id))
    
@app.route('/view_set_questions/delete_q_of_set/<int:id>')
@login_required
def delete_q_of_set(id):
    problem=quiz.query.get_or_404(id)
    db.session.delete(problem)
    db.session.commit()
    return redirect(url_for('add_set'))

@app.route('/view_set_questions/edit_q_of_set/<int:id>',methods=['GET', 'POST'])
@login_required
def edit_q_of_set(id):
    
    problem=quiz.query.get_or_404(id)
    if request.method=='POST':
        problem.quiz_name=request.form['name']
        problem.time_limit=request.form['timelimit']
        db.session.commit()
        return redirect(url_for('add_set'))
    else:
        return render_template('edit_q_of_set.html',quiz=problem)
    


@app.route('/add_set/view_set_questions/<int:id>',methods=['GET', 'POST'])
@login_required
def view_set_questions(id):
    all_problems=quiz.query.filter_by(setid=id).all()
    return render_template('view_set_questions.html',problems=all_problems)

@app.route('/view_set_questions/answer_q_of_set/<int:id>',methods=['GET', 'POST'])
def answer_q_of_set(id):
    if request.method=='POST':
        answer=request.form['answer']
        problemname=quiz.query.get_or_404(id).quiz_name
        problemset=quiz.query.get_or_404(id).setname
        new_solution=Solution(Solution=answer,problem_id=quiz.query.get_or_404(id).id,problem_answered_by=current_user.username,problemname=problemname,setname=problemset)
        db.session.add(new_solution)
        db.session.commit()
        return redirect('/add_set')
    else:
        problem=quiz.query.get_or_404(id)
        return render_template('answer_q_of_set.html',question=problem)

@app.route('/view_sets')
@login_required
def view_sets():
    all_sets=Set.query.all()
    return render_template('view_sets.html',sets=all_sets)

@app.route('/view_sets/see_set_questions/<int:id>',methods=['GET', 'POST'])
def see_set_questions(id):
    all_problems=quiz.query.filter_by(setid=id)
    return render_template('see_set_questions.html',problems=all_problems)

@app.route('/see_set_questions/answer_set_question/<int:id>',methods=['GET', 'POST'])
@login_required
def answer_set_question(id):
    if request.method=='POST':
        answer=request.form['answer']
        problemname=quiz.query.get_or_404(id).quiz_name
        problemset=quiz.query.get_or_404(id).setname
        new_solution=Solution(Solution=answer,problem_id=quiz.query.get_or_404(id).id,problem_answered_by=current_user.username,problemname=problemname,setname=problemset)
        db.session.add(new_solution)
        db.session.commit()
        return redirect('/view_sets')
    else:
        problem=quiz.query.get_or_404(id)
        sol=Solution.query.filter_by(problem_id=id,problem_answered_by=current_user.username).limit(1)
        
        return render_template('answer_set_question.html',question=problem,prevsol=sol)
    
@app.route('/view_all_answers_for_admin')
@login_required
def view_all_answers_for_admin():
    if current_user.username!='Admin':
        return render_template('accessdenied.html')
    else:
         all_answers=Solution.query.all()
         return render_template('view_all_answers_for_admin.html', data=all_answers)
     
@app.route('/view_all_answers_for_admin/delete_all_answers/<int:id>')
@login_required
def delete_all_answers(id):
    sol=Solution.query.get_or_404(id)
    db.session.delete(sol)
    db.session.commit()
    return redirect(url_for('view_all_answers_for_admin'))

@app.route('/manage_users')
@login_required
def manage_users():
    if(current_user.username=='Admin'):
        all_users=User.query.all()
        return render_template('manage_users.html',users=all_users)
    
@app.route('/manage_users/delete_user/<int:id>')
@login_required
def delete_user(id):
    user=User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))

@app.route('/add_feedback',methods=['GET','POST'])
@login_required
def add_feedback():
    if(current_user.username=='Admin'):
        if request.method=='POST':
            feedback_title=request.form['title']
            feedback_content=request.form['content']
            feedback_regarding=request.form['user']
            feedback_set=request.form['set']
            new_feedback=Feedback(title=feedback_title,content=feedback_content,feedback_for=feedback_regarding,setname=feedback_set)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(url_for('add_feedback'))
        else:
            all_feedback= Feedback.query.order_by(Feedback.timestamp).all()
            all_users=User.query.all()
            all_sets=Set.query.all()
        return render_template('add_feedback.html',feedback=all_feedback,users=all_users,sets=all_sets)
    else:
        return render_template('accessdenied.html')
    
@app.route('/add_feedback/delete_feedback/<int:id>',methods=['GET','POST'])
def delete_feedback(id):
        feedback=Feedback.query.get_or_404(id)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(url_for('add_feedback'))
    
    
@app.route('/add_tasks_individuals',methods=['GET','POST'])
@login_required
def add_tasks_individuals():
    if current_user.username=='Admin':
        if request.method=='POST':
            task_title=request.form['title']
            task_notes=request.form['sidenotes']
            task_for=request.form['user']
            task_modules=request.form['set']
            task_due_date=request.form['duedate']
            new_task=Tasks(title=task_title,side_notes=task_notes,task_for=task_for,task_set=task_modules,task_completed_by_date=task_due_date)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/add_tasks_individuals')

        else:
            all_tasks=Tasks.query.all()
            all_sets=Set.query.all()
            all_users=User.query.all()
            return render_template('add_tasks_individuals.html',tasks=all_tasks,sets=all_sets,users=all_users)
    
    else:
        return render_template('accessdenied.html')
    
@app.route('/add_tasks_individuals/delete_task/<int:id>')
@login_required
def delete_task(id):
    task=Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/add_tasks_individuals')

@app.route('/view_tasks')
@login_required
def view_tasks():
    user_tasks=Tasks.query.filter_by(task_for=current_user.username).all()
    return render_template('view_tasks.html',tasks=user_tasks)   


@app.route('/view_feedback')
@login_required
def view_feedback():
    all_feedback2= Feedback.query.filter_by(feedback_for=current_user.username).all()
    return render_template('view_feedback.html',feedback=all_feedback2)

@app.route('/apt_quiz', methods=['GET', 'POST'])
@login_required
def apt_quiz():
    all_apt=Aptitude.query.all()
    return render_template('apt_quiz.html',apt=all_apt)

@app.route('/apt_quiz/answer_apt_q/<int:id>', methods=['GET', 'POST'])
@login_required
def answer_apt_q(id):
    pull = Aptitude.query.get_or_404(id)
    form = Quiz()
    form.question.label = pull.question
    form.question.choices = [(pull.option_one,pull.option_one),(pull.option_two,pull.option_two),(pull.option_three,pull.option_three),(pull.option_four,pull.option_four),(pull.option_five,pull.option_five)]
    if form.validate_on_submit():
        f=AptAnswer(apt_answered_by=current_user.username,apt_question=form.question.label,apt_choice=form.question.data)
        db.session.add(f)
        db.session.commit()
        return redirect(url_for('apt_quiz'))
   
    return render_template('answer_aptitude_quiz.html',form=form,question=Aptitude.query.get_or_404(id))

@app.route('/aptitude_answers')
@login_required
def aptitude_answers(): 
    data=AptAnswer.query.all()
    return render_template('aptitude_answers.html',data=data)  

@app.route('/aptitude_answers/delete_apt_answer/<int:id>',methods=['GET', 'POST'])
@login_required
def delete_apt_answer(id):
    data=AptAnswer.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('aptitude_answers'))

 
@app.route('/add_data_for_aptitude', methods=['GET', 'POST'])
@login_required
def add_data_for_aptitude():
    if current_user.username=='Admin':
        if request.method=='POST':
            apt_question=request.form['question']
            apt_option1=request.form['option1']
            apt_option2=request.form['option2']
            apt_option3=request.form['option3']
            apt_option4=request.form['option4']
            apt_option5=request.form['option5']
            new_apt=Aptitude(question=apt_question,option_one=apt_option1,option_two=apt_option2,option_three=apt_option3,option_four=apt_option4,option_five=apt_option5)
            db.session.add(new_apt)
            db.session.commit()
            return redirect(url_for('add_data_for_aptitude'))           
        else:
            all_apt=Aptitude.query.all()
            return render_template('add_data_for_aptitude.html',apt=all_apt)
    else:
        return render_template('accessdenied.html')
    
@app.route('/add_data_for_aptitude/delete_apt_question/<int:id>')
@login_required
def delete_apt_question(id):
    apt_question=Aptitude.query.get_or_404(id)
    db.session.delete(apt_question)
    db.session.commit()
    return redirect(url_for('add_data_for_aptitude'))

@app.route('/add_data_for_aptitude/edit_apt_question/<int:id>',methods=['GET', 'POST'])
def edit_apt_question(id):
    apt_question=Aptitude.query.get_or_404(id)
    if request.method=='POST':
        apt_question.question=request.form['question']
        apt_question.option_one=request.form['option1']
        apt_question.option_two=request.form['option2']
        apt_question.option_three=request.form['option3']
        apt_question.option_four=request.form['option4']
        apt_question.option_five=request.form['option5']
        db.session.commit()
        return redirect(url_for('add_data_for_aptitude'))
    else:
        return render_template('edit_apt_question.html',data=apt_question)
    
@app.route('/aptitude_answers_for_me')
@login_required
def aptitude_answers_for_me(): 
    data=AptAnswer.query.filter_by(apt_answered_by=current_user.username).all()
    return render_template('aptitude_answers_for_me.html',data=data)
    
@app.route('/verbreason_quiz', methods=['GET', 'POST'])
@login_required
def verbreason_quiz():
    all_verb=VerbReason.query.all()
    return render_template('verbreason_quiz.html',verb=all_verb)

@app.route('/verbreason_quiz/answer_verbreason/<int:id>', methods=['GET', 'POST'])
@login_required
def answer_verbreason(id):
    pull = VerbReason.query.get_or_404(id)
    form = VerbReasonform()
    form.question.label = pull.question
    form.question.choices = [(pull.option_one,pull.option_one),(pull.option_two,pull.option_two),(pull.option_three,pull.option_three)]
    if form.validate_on_submit():
        f=VerbReasonAnswer(verb_answered_by=current_user.username,verb_question=form.question.label,verb_choice=form.question.data)
        db.session.add(f)
        db.session.commit()
        return redirect(url_for('verbreason_quiz'))
   
    return render_template('answer_verbreason.html',form=form,question=VerbReason.query.get_or_404(id))

@app.route('/verbreason_answers')
@login_required
def verbreason_answers(): 
    data=VerbReasonAnswer.query.all()
    return render_template('verbreason_answers.html',data=data)

@app.route('/verbreason_answers/delete_verbreason_answers/<int:id>',methods=['GET', 'POST'])
def delete_verbreason_answers(id): 
    data=VerbReasonAnswer.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('verbreason_answers'))

@app.route('/add_data_for_verbreason', methods=['GET', 'POST'])
@login_required
def add_data_for_verbreason():
    if current_user.username=='Admin':
        if request.method=='POST':
            verb_question=request.form['question']
            verb_option1=request.form['option1']
            verb_option2=request.form['option2']
            verb_option3=request.form['option3']
            verb_option3=request.form['option3']
            verb_time_limit=request.form['timelimit']
            new_verbreason=VerbReason(question=verb_question,option_one=verb_option1,option_two=verb_option2,option_three=verb_option3,time_limit=verb_time_limit)
            db.session.add(new_verbreason)
            db.session.commit()
            return redirect(url_for('add_data_for_verbreason'))           
        else:
            verb=VerbReason.query.order_by(VerbReason.timestamp).all()
            return render_template('add_data_for_verbreason.html',verb=verb)
    else:
        return render_template('accessdenied.html')
    
@app.route('/add_data_for_verbreason/delete_verbreason_question/<int:id>',methods=['GET', 'POST'])
def delete_verbreason_question(id):
    verbreason_question=VerbReason.query.get_or_404(id)
    db.session.delete(verbreason_question)
    db.session.commit()
    return redirect(url_for('add_data_for_verbreason'))

@app.route('/add_data_for_verbreason/edit_verbreason_question/<int:id>',methods=['GET', 'POST'])
def edit_verbreason_question(id):
    verbreason_question=VerbReason.query.get_or_404(id)
    if request.method=='POST':
        verbreason_question.question=request.form['question']
        verbreason_question.option_one=request.form['option1']
        verbreason_question.option_two=request.form['option2']
        verbreason_question.option_three=request.form['option3']
        db.session.commit()
        return redirect(url_for('add_data_for_verbreason'))
    else:
        return render_template('edit_verbreason_question.html',data=verbreason_question)
  
@app.route('/my_verbreason_answers',methods=['GET','POST'])
@login_required
def my_verbreason_answers(): 
    data=VerbReasonAnswer.query.filter_by(verb_answered_by=current_user.username).all()
    return render_template('my_verbreason_answers.html',data=data)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        
        

