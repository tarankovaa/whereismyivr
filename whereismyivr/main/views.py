from django.shortcuts import redirect, render
from django.views import View
from .models import Card
from .forms import CreateCardForm


def index(request):
    all_cards = Card.objects.all()
    context = {
        'cards': all_cards,
    }
    return render(request, 'main/index.html', context)


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
            return redirect('login')
        return super(CreateCardView, self).dispatch(request, *args, **kwargs)
