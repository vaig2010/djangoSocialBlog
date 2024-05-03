from django.shortcuts import render

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

