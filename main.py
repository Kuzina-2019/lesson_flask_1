from flask import Flask, render_template
from data import db_session
from data.users import User
from data.news import News
from data.register import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.sqlite")
        
    '''user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email1@email.ru"
    session = db_session.create_session()
    session.add(user)
    session.commit() 
    
    user = User()
    user.name = "Пользователь 2"
    user.about = "биография пользователя 2"
    user.email = "email2@email.ru"
    session = db_session.create_session()
    session.add(user)
    session.commit() 
    
    user = User()
    user.name = "Пользователь 3"
    user.about = "биография пользователя 3"
    user.email = "email3@email.ru"
    session = db_session.create_session()
    session    .add(user)
    session.commit() 
    
    news = News(title="Первая новость", content="Привет блог!", 
                user_id=1, is_private=False)
    session.add(news)
    session.commit() '''    
    
    @app.route("/")    
    def index():
        session = db_session.create_session()
        news = session.query(News).filter(News.is_private != True)
        return render_template("index.html", news=news)   
    
    
    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)    
   
    app.run()

if __name__ == '__main__':
    main()