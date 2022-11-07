from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views import View
from .models import Card
from .forms import CreateCardForm, FilterForm


def index(request):
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
    cards = all_cards[:0]
    if form.cleaned_data.get('it_project'):
        cards = cards.union(all_cards.filter(field_of_card='it').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('business_project'):
        cards = cards.union(all_cards.filter(field_of_card='business').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('design'):
        cards = cards.union(all_cards.filter(field_of_card='design').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('publishing'):
        cards = cards.union(all_cards.filter(field_of_card='publishing').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('engineering'):
        cards = cards.union(all_cards.filter(field_of_card='engineering').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('media'):
        cards = cards.union(all_cards.filter(field_of_card='media').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('education_project'):
        cards = cards.union(all_cards.filter(field_of_card='education').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('events'):
        cards = cards.union(all_cards.filter(field_of_card='events').filter(type_of_card=Card.PROJECT))
    if form.cleaned_data.get('it_research'):
        cards = cards.union(all_cards.filter(field_of_card='it').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('business_research'):
        cards = cards.union(all_cards.filter(field_of_card='business').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('oriental_studies'):
        cards = cards.union(
            all_cards.filter(field_of_card='oriental_studies').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('natural_sciences'):
        cards = cards.union(
            all_cards.filter(field_of_card='natural_sciences').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('art'):
        cards = cards.union(all_cards.filter(field_of_card='art').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('history'):
        cards = cards.union(all_cards.filter(field_of_card='history').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('culturology'):
        cards = cards.union(all_cards.filter(field_of_card='culturology').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('marketing'):
        cards = cards.union(all_cards.filter(field_of_card='marketing').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('maths'):
        cards = cards.union(all_cards.filter(field_of_card='maths').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('management'):
        cards = cards.union(
            all_cards.filter(field_of_card='management').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('linguistics'):
        cards = cards.union(all_cards.filter(field_of_card='linguistics').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('education_research'):
        cards = cards.union(all_cards.filter(field_of_card='education').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('politics'):
        cards = cards.union(all_cards.filter(field_of_card='politics').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('right'):
        cards = cards.union(all_cards.filter(field_of_card='right').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('psychology'):
        cards = cards.union(all_cards.filter(field_of_card='psychology').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('sociology'):
        cards = cards.union(all_cards.filter(field_of_card='sociology').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('philology'):
        cards = cards.union(all_cards.filter(field_of_card='philology').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('philosophy'):
        cards = cards.union(all_cards.filter(field_of_card='philosophy').filter(type_of_card=Card.RESEARCH))
    if form.cleaned_data.get('economy'):
        cards = cards.union(all_cards.filter(field_of_card='economy').filter(type_of_card=Card.RESEARCH))
    return cards


class CreateCardView(View):
    form_class = CreateCardForm
    template_name = 'main/create_card.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
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
