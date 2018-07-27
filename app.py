from flask import Flask,render_template,request,redirect,url_for,session,g
import config
from models import User,Question,Answer
from exts import db
from decorators import login_requried
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter(User.email==email).first()

        if user and user.check_password(password):
            session['user_id']=user.id
            #31天不需要登录
            session.parmant=True
            return redirect(url_for('index'))
        else:
            return u"登录名或密码错误"


@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter(User.email==email).first()
        if user:
            return u"emial已存在请直接登录"
        else:
            if password1!=password2:
                return u"两次密码不一致请重新输入"
            else:
                user=User(email=email,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))



@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=question_model)

@app.route('/question/',methods=['GET','POST'])
def question():
    if request.method=='GET':
        context={
            'questions':Question.query.order_by('id').all( )
        }
        return render_template('question.html',**context)
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        question.author=g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question'))

@app.route('/add_answer/',methods=['POST'])
@login_requried
def add_answer():
    content=request.form.get('answer_content')
    question_id=request.form.get('question_id')

    answer=Answer(content=content)

    answer.author=g.user
    question=Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q=request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-id')
    return render_template('question.html',questions=questions)

@app.before_request
def my_before_request():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            g.user=user

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):      #函数判断属性g有没有user对象
        return {'user': g.user}
    return {}
#befor_request-->视图函数-->context_processor
"""
@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return{'user':user}
    return {}
"""
@app.route('/logout/')
def logout():
    #session.pop('user_id')
    #del session['user_id']
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()