from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user, login_user

from users.models import User
from .forms import RegistrationForm, UserLoginForm, UserProfileForm

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
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            user.save()
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
            user = User.objects.get(username=form.username.data)
            if user:
                if user.check_password(form.password.data):
                    user.authenticated = True
                    user.save()
                    login_user(user, remember=True)
                    return redirect('/')
        return render_template(self.template_name, form=form)


class UserProfileView(MethodView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(request.form)
        if form.validate():
            current_user.address = form.address.data
            current_user.address_lat = form.address_lat.data
            current_user.address_lng = form.address_lng.data
            current_user.save()
            flash('Profile updated')
            return redirect('/')
        return render_template(self.template_name, form=form)


@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    user.save()
    logout_user()
    return redirect('/')


users.add_url_rule("/sign_up/",
                   view_func=UserRegistrationView.as_view('sign_up'))
users.add_url_rule("/login/", view_func=UserLoginView.as_view('login'))
users.add_url_rule("/profile/", view_func=UserProfileView.as_view('profile'))
users.add_url_rule("/logout/", view_func=UserRegistrationView.as_view('logout'))
