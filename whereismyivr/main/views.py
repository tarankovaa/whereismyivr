from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views import View
from .models import Card
from .forms import CreateCardForm


def index(request):
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        cards = []
        # form = None
    else:
        # form = FilterForm(request.post)
        # if form.it.
        cards = Card.objects.order_by('-created_on')
    return render(request, 'main/index.html', {'cards': cards,
                                               'search': None})


def search(request, param):
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        cards = []
    else:
        if param == "customer":
            cards = Card.objects.order_by('-created_on').filter(customer=True)
        elif param == "consultant":
            cards = Card.objects.order_by('-created_on').filter(consultant=True)
        elif param == "performer":
            cards = Card.objects.order_by('-created_on').filter(performer=True)
        elif param == "partner":
            cards = Card.objects.order_by('-created_on').filter(partner=True)
    return render(request, 'main/index.html', {'cards': cards,
                                               'search': param})


'''def consultant(request):
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        cards = []
    else:
        cards = Card.objects.order_by('-created_on').filter(consultant=True)
    return render(request, 'main/index.html', {'cards': cards,
                                               'search': 'consultant'})


def performer(request):
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        cards = []
    else:
        cards = Card.objects.order_by('-created_on').filter(performer=True)
    return render(request, 'main/index.html', {'cards': cards,
                                               'search': 'performer'})


def partner(request):
    if not request.user.is_authenticated:
        messages.error(request, mark_safe('<a href="/login">Войдите</a>, чтобы просматривать заявки'))
        cards = []
    else:
        cards = Card.objects.order_by('-created_on').filter(partner=True)
    return render(request, 'main/index.html', {'cards': cards,
                                               'search': 'partner'})'''


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
