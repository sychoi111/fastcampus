from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    username = forms.CharField(
        error_messages={"required": "유저이름을 입력해주세요."},
        label="유저명",
    )
    password1 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )
    password2 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호 확인",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={"required" : "유저명을 입력해주세요."}, max_length=32, label = "유저명")
    password = forms.CharField(error_messages={"required" : "비밀번호를 입력해주세요."}, max_length=64, label = "비밀번호", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if password and username:
            try:
                users = User.objects.get(username = username)
            except User.DoesNotExists:
                self.add_error("username", "유저명이 존재하지 않습니다.")
                return
            if not check_password(password, users.password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")
            else:
                self.id = users.id

