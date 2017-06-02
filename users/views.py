from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user, login_user

from database import db
from users.models import User
from .forms import RegistrationForm, UserLoginForm

users = Blueprint("users", __name__)


class UserRegistrationView(MethodView):
    form_class = RegistrationForm
    template_name = 'users/sign_up.html'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(request.form)
        if form.validate():
            user = User(form.username.data, form.email.data,
                        form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering')
            return redirect(url_for('users.login'))
        return render_template(self.template_name, form=form)


class UserLoginView(MethodView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True)
                    return redirect('/')
        return render_template(self.template_name, form=form)


@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/')


users.add_url_rule("/sign_up/",
                   view_func=UserRegistrationView.as_view('sign_up'))
users.add_url_rule("/login/", view_func=UserLoginView.as_view('login'))
users.add_url_rule("/logout/", view_func=UserRegistrationView.as_view('logout'))
