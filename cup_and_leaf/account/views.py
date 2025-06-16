from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from tea_collection.models import TeaPost


@login_required
def profile(request):
    if request.method == "POST":
        # Обновление данных пользователя
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        # Обновление профиля
        profile = user.profile
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
        profile.bio = request.POST.get("bio")
        profile.save()

        messages.success(request, "Профиль успешно обновлен")
        return redirect("account:profile")

    # Получение постов пользователя
    user_posts = TeaPost.objects.filter(author=request.user).order_by("-created_at")

    context = {
        "user_posts": user_posts,
    }
    return render(request, "account/profile.html", context)
