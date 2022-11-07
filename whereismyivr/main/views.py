from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views import View

from .models import Card
from .forms import FilterForm, CreateCardForm


def index(request):
    # обработка главной страницы (вывод всех заявок и фильтрация)
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        return render(request, 'main/home.html', {'cards': [],
                                                  'form': None,
                                                  'search': None})
    else:
        all_cards = Card.objects.order_by('-created_on')
        form = FilterForm()
        cards = all_cards
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            cards = get_cards(form, all_cards)
        else:
            messages.error(request, "Что-то пошло не так")
    return render(request, 'main/home.html', {'cards': cards,
                                              'form': form,
                                              'search': None})


def search(request, param):
    # поиск по должностям
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        return render(request, 'main/home.html', {'cards': [],
                                                  'form': None,
                                                  'search': param})
    else:
        if param == "customer":
            all_cards = Card.objects.order_by('-created_on').filter(customer=True)
        elif param == "consultant":
            all_cards = Card.objects.order_by('-created_on').filter(consultant=True)
        elif param == "performer":
            all_cards = Card.objects.order_by('-created_on').filter(performer=True)
        elif param == "partner":
            all_cards = Card.objects.order_by('-created_on').filter(partner=True)
        else:
            return redirect('home')
        form = FilterForm()
        cards = all_cards
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            cards = get_cards(form, all_cards)
        else:
            messages.error(request, "Что-то пошло не так")
    return render(request, 'main/home.html', {'cards': cards,
                                              'search': param,
                                              'form': form})


def get_cards(form, all_cards):
    # получить заявки, соответствующие фильтрации
    cards = all_cards[:0]
    count = 0
    for value in Card.KEYS_TYPE_OF_FIELD_CHOICES:
        if value in form.data:
            count += 1
            cards = cards.union(all_cards.filter(field_of_card=value))
    if not count:
        return all_cards
    return cards


class CreateCardView(View):
    # создание заявки
    form_class = CreateCardForm
    template_name = 'main/create_card.html'

    def get(self, request, *args, **kwargs):
        # обработка гет-запроса
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # обработка данных из формы, добавление заявки в базу данных
        form = self.form_class(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            if not (card.customer or card.partner or card.consultant or card.performer):
                errors = ["Выберите, кого вы ищете"]
                return render(request, self.template_name, {'form': form,
                                                            'errors': errors})

            if request.user.profile.is_performer() and card.get_type_of_card() == card.RESEARCH and (
                    card.customer or card.partner):
                messages.error(request, "Поиск заказчика и/или напарника недоступен для заявок типа исследование")
                return render(request, self.template_name, {'form': form})

            if request.user.profile.is_customer() and card.get_type_of_card() == card.RESEARCH:
                messages.error(request, "Поиск исполнителя доступен только для работ типа проект")
                return render(request, self.template_name, {'form': form})
            card.user = request.user
            card.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # ограничения на работу со страницей
        if not request.user.is_authenticated:
            return redirect('/login/?next=/create-card/')
        if not request.user.profile.is_filled:
            messages.error(request, mark_safe("""Создание заявки возможно только с заполненным профилем.
            Заполните его во вкладке <a href="/profile">профиль</a>"""))
            return redirect('home')
        if request.user.profile.profile_type == "CO":
            messages.error(request, mark_safe("""Ваш тип пользователя не позволяет создать карточку. 
            Вы можете поменять его в настройках <a href="/profile">профиля</a>"""))
            return redirect('home')
        return super(CreateCardView, self).dispatch(request, *args, **kwargs)
