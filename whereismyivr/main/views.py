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
    if form.cleaned_data.get('it_project'):
        cards = cards.union(all_cards.filter(field_of_card='it_project'))
    if form.cleaned_data.get('business_project'):
        cards = cards.union(all_cards.filter(field_of_card='business_project'))
    if form.cleaned_data.get('design'):
        cards = cards.union(all_cards.filter(field_of_card='design'))
    if form.cleaned_data.get('publishing'):
        cards = cards.union(all_cards.filter(field_of_card='publishing'))
    if form.cleaned_data.get('engineering'):
        cards = cards.union(all_cards.filter(field_of_card='engineering'))
    if form.cleaned_data.get('media'):
        cards = cards.union(all_cards.filter(field_of_card='media'))
    if form.cleaned_data.get('education_project'):
        cards = cards.union(all_cards.filter(field_of_card='education_project'))
    if form.cleaned_data.get('events'):
        cards = cards.union(all_cards.filter(field_of_card='events'))
    if form.cleaned_data.get('it_research'):
        cards = cards.union(all_cards.filter(field_of_card='it_research'))
    if form.cleaned_data.get('business_research'):
        cards = cards.union(all_cards.filter(field_of_card='business_research'))
    if form.cleaned_data.get('oriental_studies'):
        cards = cards.union(
            all_cards.filter(field_of_card='oriental_studies'))
    if form.cleaned_data.get('natural_sciences'):
        cards = cards.union(
            all_cards.filter(field_of_card='natural_sciences'))
    if form.cleaned_data.get('art'):
        cards = cards.union(all_cards.filter(field_of_card='art'))
    if form.cleaned_data.get('history'):
        cards = cards.union(all_cards.filter(field_of_card='history'))
    if form.cleaned_data.get('culturology'):
        cards = cards.union(all_cards.filter(field_of_card='culturology'))
    if form.cleaned_data.get('marketing'):
        cards = cards.union(all_cards.filter(field_of_card='marketing'))
    if form.cleaned_data.get('maths'):
        cards = cards.union(all_cards.filter(field_of_card='maths'))
    if form.cleaned_data.get('management'):
        cards = cards.union(
            all_cards.filter(field_of_card='management'))
    if form.cleaned_data.get('linguistics'):
        cards = cards.union(all_cards.filter(field_of_card='linguistics'))
    if form.cleaned_data.get('education_research'):
        cards = cards.union(all_cards.filter(field_of_card='education_research'))
    if form.cleaned_data.get('politics'):
        cards = cards.union(all_cards.filter(field_of_card='politics'))
    if form.cleaned_data.get('right'):
        cards = cards.union(all_cards.filter(field_of_card='right'))
    if form.cleaned_data.get('psychology'):
        cards = cards.union(all_cards.filter(field_of_card='psychology'))
    if form.cleaned_data.get('sociology'):
        cards = cards.union(all_cards.filter(field_of_card='sociology'))
    if form.cleaned_data.get('philology'):
        cards = cards.union(all_cards.filter(field_of_card='philology'))
    if form.cleaned_data.get('philosophy'):
        cards = cards.union(all_cards.filter(field_of_card='philosophy'))
    if form.cleaned_data.get('economy'):
        cards = cards.union(all_cards.filter(field_of_card='economy'))
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
            messages.error(request, """Ваш тип пользователя не позволяет создать карточку. 
            Вы можете поменять его в настройках <a href="/profile">профиля</a>""")
            return redirect('home')
        return super(CreateCardView, self).dispatch(request, *args, **kwargs)
