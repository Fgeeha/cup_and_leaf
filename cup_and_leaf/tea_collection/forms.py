from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import slugify
from datetime import datetime

from .models import TeaPost, TeaComment

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш email"}
        ),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите ваше имя"}
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите вашу фамилию"}
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        )
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email"
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        base_username = slugify(
            f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        )
        username = base_username or "user"
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email",
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean_username(self):
        email = self.cleaned_data.get("username")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["password"].label = "Пароль"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "Email",
        }
        help_texts = {
            "username": (
                "Обязательное. Не более 150 символов. "
                "Используйте только буквы, цифры и символы @/./+/-/_."
            )
        }


class TeaPostForm(forms.ModelForm):
    class Meta:
        model = TeaPost
        fields = [
            "title",
            "type",
            "origin",
            "production_year",
            "tea_grade",
            "appearance",
            "description",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "type": forms.Select(attrs={"class": "form-control"}),
            "origin": forms.Select(attrs={"class": "form-control"}),
            "production_year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Год производства"}
            ),
            "tea_grade": forms.Select(attrs={"class": "form-control"}),
            "appearance": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Опишите внешний вид...",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Введите описание...",
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class TeaCommentForm(forms.ModelForm):
    class Meta:
        model = TeaComment
        fields = ["text", "rating"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Оставьте ваш комментарий...",
                }
            ),
            "rating": forms.Select(attrs={"class": "form-control"}),
        }


class TeaSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Поиск по названию..."}
        ),
    )
    type = forms.ChoiceField(
        required=False,
        choices=[("", "Все типы")] + TeaPost.TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    origin = forms.ChoiceField(
        required=False,
        choices=[("", "Все регионы")] + TeaPost.ORIGIN_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    current_year = datetime.now().year
    production_year = forms.ChoiceField(
        required=False,
        choices=[("", "Все годы")]
        + [(year, year) for year in range(2020, current_year + 1)],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    tea_grade = forms.ChoiceField(
        required=False,
        choices=[("", "Все сорта")] + TeaPost.TEA_GRADE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    appearance = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Поиск по внешнему виду..."}
        ),
    )
