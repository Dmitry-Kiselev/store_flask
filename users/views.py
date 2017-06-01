from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask.views import View, MethodView
from flask_login import login_required, current_user, logout_user, login_user

from database import db_session
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
            db_session.add(user)
            flash('Thanks for registering')
            return redirect(url_for('login'))
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
            user = User.query.get(form.username.data)
            if user:
                if user.password == form.password.data:
                    user.authenticated = True
                    db_session.add(user)
                    db_session.commit()
                    login_user(user, remember=True)
                    return redirect(url_for("/"))
        return render_template(self.template_name, form=form)


@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return redirect('/')


users.add_url_rule("/sign_up/", view_func=UserRegistrationView.as_view('sign_up'))
users.add_url_rule("/login/", view_func=UserLoginView.as_view('login'))
users.add_url_rule("/logout/", view_func=UserRegistrationView.as_view('logout'))

