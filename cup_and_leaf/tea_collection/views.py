from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .forms import (
    TeaCommentForm,
    UserEditForm,
    CustomUserCreationForm,
    TeaSearchForm,
    CustomAuthenticationForm,
)
from .models import TeaPost, TeaComment, User
from .utils import send_welcome_email


class TeaPostListView(ListView):
    model = TeaPost
    template_name = "tea_collection/index.html"
    context_object_name = "tea_posts"
    paginate_by = 9

    def get_queryset(self):
        queryset = TeaPost.objects.all()
        search_form = TeaSearchForm(self.request.GET)
        if search_form.is_valid():
            if search_form.cleaned_data.get("query"):
                queryset = queryset.filter(
                    title__icontains=search_form.cleaned_data["query"]
                )
            if search_form.cleaned_data.get("type"):
                queryset = queryset.filter(type=search_form.cleaned_data["type"])
            if search_form.cleaned_data.get("origin"):
                queryset = queryset.filter(origin=search_form.cleaned_data["origin"])
            if search_form.cleaned_data.get("production_year"):
                queryset = queryset.filter(
                    production_year=search_form.cleaned_data["production_year"]
                )
            if search_form.cleaned_data.get("tea_grade"):
                queryset = queryset.filter(
                    tea_grade=search_form.cleaned_data["tea_grade"]
                )
            if search_form.cleaned_data.get("appearance"):
                queryset = queryset.filter(
                    appearance__icontains=search_form.cleaned_data["appearance"]
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TeaSearchForm(self.request.GET)
        context["tea_types"] = TeaPost.TYPE_CHOICES
        context["tea_origins"] = TeaPost.ORIGIN_CHOICES
        context["tea_grades"] = TeaPost.TEA_GRADE_CHOICES
        context["production_years"] = [(year, year) for year in range(2020, 2025)]
        return context


class TeaPostDetailView(DetailView):
    model = TeaPost
    template_name = "tea_collection/tea_post_detail.html"
    context_object_name = "tea"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = TeaCommentForm()
        context["comments"] = self.object.comments.select_related("author").all()
        return context


class TeaPostCreateView(LoginRequiredMixin, CreateView):
    model = TeaPost
    template_name = "tea_collection/tea_post_form.html"
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
    success_url = reverse_lazy("tea_collection:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TeaPostUpdateView(LoginRequiredMixin, UpdateView):
    model = TeaPost
    template_name = "tea_collection/tea_post_form.html"
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

    def get_queryset(self):
        return TeaPost.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("tea_collection:tea_detail", kwargs={"pk": self.object.pk})


class TeaPostDeleteView(LoginRequiredMixin, DeleteView):
    model = TeaPost
    template_name = "tea_collection/tea_post_confirm_delete.html"
    success_url = reverse_lazy("tea_collection:index")

    def get_queryset(self):
        return TeaPost.objects.filter(author=self.request.user)


@login_required
def add_comment(request, pk):
    tea_post = get_object_or_404(TeaPost, pk=pk)
    if request.method == "POST":
        form = TeaCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tea_post = tea_post
            comment.author = request.user
            comment.save()
    return redirect("tea_collection:tea_detail", pk=pk)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("tea_collection:index")
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "tea_collection/profile_edit.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("username")
        try:
            user = User.objects.get(email=email)
            form.cleaned_data["username"] = user.username
        except User.DoesNotExist:
            pass
        return super().form_valid(form)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Отправляем приветственное письмо
            try:
                send_welcome_email(user)
                messages.success(
                    request,
                    f"Добро пожаловать, {user.first_name}! Ваш аккаунт успешно создан.",
                )
            except Exception:
                messages.warning(
                    request,
                    "Аккаунт создан, но возникла проблема с отправкой приветственного письма.",
                )
            return redirect("tea_collection:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(TeaComment, pk=comment_pk, tea_post_id=pk)
    if comment.author == request.user:
        comment.delete()
    return redirect("tea_collection:tea_detail", pk=pk)


@login_required
def profile(request):
    user = request.user
    tea_posts = TeaPost.objects.filter(author=user).order_by("-created_at")
    comments = TeaComment.objects.filter(author=user).order_by("-created_at")

    context = {
        "user": user,
        "tea_posts": tea_posts,
        "comments": comments,
    }
    return render(request, "tea_collection/profile.html", context)


def search_tea(request):
    form = TeaSearchForm(request.GET)
    tea_posts = TeaPost.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            tea_posts = tea_posts.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(type__icontains=query)
                | Q(origin__icontains=query)
                | Q(appearance__icontains=query)
            ).distinct()

    paginator = Paginator(tea_posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "page_obj": page_obj,
        "query": request.GET.get("query", ""),
    }
    return render(request, "tea_collection/search_results.html", context)
