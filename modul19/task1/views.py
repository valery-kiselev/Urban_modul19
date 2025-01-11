from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *
from django.core.paginator import Paginator


# Create your views here.
def platform(request):
    return render(request, 'templ1/platform.html')

def games(request):
#    games = ["Atomic Heart", "Cyberpunk 2077"]
    games = Game.objects.all()
    return render(request, 'templ1/games.html', {'games': games})

def cart(request):
    return render(request, 'templ1/cart.html')

def news(request):
    news = News.objects.all().order_by('date')
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page')
    page_news = paginator.get_page(page_number)
    return render(request, 'templ1/news.html', {'news':page_news})

def sign_up_by_html(request):
    users = Buyer.objects.all()
    info = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        for user in users:
            if user.name == username:
                info['error'] = "Пользователь уже существует"
                return HttpResponse('Пользователь уже существует')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))

        if password != repeat_password:
            info['error'] = "Пароли не совпадают"
            return HttpResponse('Пароли не совпадают')
        elif age < 18:
            info['error'] = "Вы должны быть старше 18"
            return HttpResponse('Вы должны быть старше 18')
        else:
            Buyer.objects.create(name=username, age=age, balance=100)
            info['welcome_message'] = f"Приветствуем, {username}!"  # Приветственное сообщение

        return HttpResponse(f"Приветствуем, {username}!")
    return render(request, 'templ1/registration_page.html', context=info)

def sign_up_by_django(request):
    users = Buyer.objects.all()
    info = {}
    form = UserRegister()

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            for user in users:
                if user.name == username:
                    # info['error'] = "Пользователь уже существует"
                    return HttpResponse('Пользователь уже существует')

            # if username in users:
            #     info['error'] = 'Пользователь уже существует'
            if password != repeat_password:
                # info['error'] = 'Пароли не совпадают'
                return HttpResponse('Пароли не совпадают')
            elif age < 18:
                # info['error'] = 'Вы должны быть старше 18'
                return HttpResponse('Вы должны быть старше 18')
            else:
                Buyer.objects.create(name=username, age=age, balance=100)
                # info['message'] = f'Приветствуем, {username}!'
                return HttpResponse(f"Приветствуем, {username}!")

        # info['form'] = form

    return render(request, 'templ1/registration_page.html', context=info)