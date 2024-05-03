from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from socialblog.forms import BlogForm, CommentForm, LoginForm
from socialblog.models import Blog, Comment

def get_base_menu():
    return [
        {"link": "/", "text": "Главная"},
        {"link": "/blog/", "text": "Страница с блогами"},
    ]

def index_page(request):
    context = {
        "page_name": "Главная",
        "menu_items": get_base_menu(),
    }
    return render(request, "index_page.html", context)

def blog_page(request):
    context = {
        "page_name": "Страница с блогами",
        "menu_items": get_base_menu(),
        "comment_form": CommentForm(),
    }
    blog_items = Blog.objects.all().values()
    
    for index in range(len(blog_items)):
        blog_items[index]["author"] = User.objects.get(id=blog_items[index]["author_id"])
        blog_items[index]["comment_items"] = Comment.objects.filter(blog_id=Blog.objects.get(id=blog_items[index]["id"])).values()
    
    context["blog_items"] = blog_items

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.save(Blog.objects.get(id=request.GET.get("blog_id")))

    return render(request, "blog_page.html", context)


def registration_page(request):
    context = {
        "page_name": "Регистрация нового пользователя",
        "menu_items": get_base_menu(),
    }

    if request.method == "POST":
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

            username = user_creation_form.cleaned_data.get("username")
            password = user_creation_form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("/")
    else:
        user_creation_form = UserCreationForm()

    context["user_creation_form"] = user_creation_form

    return render(request, "account_pages/registration_page.html", context)


# По сути написали свой вход в систему
def login_page(request):
    context = {
        "page_name": "Вход в систему",
        "menu_items": get_base_menu(),
    }

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:  # Если пользователя нет в системе
                login(request, user)
                return redirect("/")
            else:
                context["login_error"] = True
    else:
        login_form = LoginForm()

    context["login_form"] = login_form

    return render(request, "account_pages/login_page.html", context)


# По сути написали свой выход из системы
@login_required
def logout_page(request):
    logout(request)

    return redirect("/")


@login_required
def blog_add_page(request):
    context = {
        "page_name": "Добавление статьи",
        "menu_items": get_base_menu(),
    }

    if request.method == "POST":
        blog_form = BlogForm(request.POST)
        blog_form.save(request.user)
        context["blog_added"] = True
    else:
        blog_form = BlogForm()

    context["blog_form"] = blog_form

    return render(request, "blog_add_page.html", context)
