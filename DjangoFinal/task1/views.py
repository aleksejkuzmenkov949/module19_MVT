from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import Buyer
from .models import Game


# Create your views here.
def platform(request):    return render(request, 'platform.html')


def games(request):
    # Получаем все записи из таблицы Game
    items = Game.objects.all()

    # Передаем коллекцию в контекст рендеринга
    context = {'items': items}
    return render(request, 'games.html', context)


def cart(request):
    return render(request, 'cart.html')


def sign_up_by_html(request):
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        # Выводим информацию в консоль
        print(f'Полученные данные: username={username}, age={age}')

        # Проверяем, существует ли пользователь с таким именем
        if Buyer.objects.filter(name=username).exists():
            info['error'] = 'Пользователь уже существует'
            print(info['error'])

        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
            print(info['error'])

        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают'
            print(info['error'])

        else:
            # Создаем нового покупателя
            new_buyer = Buyer.objects.create(name=username, balance=0, age=int(age))

            print(f'Приветствуем, {new_buyer.name} !')
            return render(request, 'registration_page.html', {'username': username})

    return render(request, 'registration_page.html', {'info': info})


def sign_up_by_django(request):
    users = ['Alex', 'Darja', 'Cat31']
    info = {}

    if request.method == 'POST':
        form = UserRegister(request.POST)

        # Проверяем, валидна ли форма
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            try:
                age = int(form.cleaned_data['age'])

                # Проверка на несовпадение паролей
                if password != repeat_password:
                    form.add_error('repeat_password', 'Пароли не совпадают')
                elif age < 18:
                    form.add_error('age', 'Вы должны быть старше 18 лет')
                elif username in users:
                    form.add_error('username', 'Пользователь уже существует')
                else:
                    info['success'] = f"Приветствуем, {username}!"
                    # Возвращаем объект HttpResponse с приветственным сообщением
                    return HttpResponse(info['success'])

            except ValueError:
                form.add_error('age', 'Введите корректное число для возраста')

        # Если форма невалидна, выводим ошибки формы
        info['form_errors'] = form.errors
    else:
        form = UserRegister()

    info['form'] = form
    return render(request, 'sign_up.html', info)
