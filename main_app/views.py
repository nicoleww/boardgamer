from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Game, Review, Wishlist


# RENDER PAGES

def home(request):
    return render(request, 'home.html')


def games_index(request):
    games = Game.objects.all()
    return render(request, 'games/index.html', {'games': games})


def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    review = Review.objects.filter(game_id=game_id)
    return render(request, 'games/detail.html', {'game': game, 'review': review})


@login_required
def my_games(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/my-games.html', {'games': games})


@login_required
def create(request):
    return render(request, 'games/create_form.html')


@login_required
def edit(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'games/edit_form.html', {'game': game})


@login_required
def render_wishlist(request):
    try:
        items = Wishlist.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'items': items})
    except:
        return render(request, 'wishlist.html')


def search(request):
    g_name = request.POST['name']
    games = Game.objects.filter(name=g_name)
    return render(request, 'games/result.html', {'games': games})


def render_search(request):
    return render(request, 'games/search.html')


# CREATE


@login_required
def submit_create(request):
    Game.objects.create(
        name=request.POST['name'],
        publisher=request.POST['publisher'],
        players=request.POST['players'],
        description=request.POST['description'],
        user=request.user,
    )
    return redirect('/games/')


@login_required
def review_form(request, game_id):
    Review.objects.create(
        rating=request.POST['rating'],
        text=request.POST['text'],
        game_id=game_id
    )
    return redirect(f'/games/{game_id}/')


@login_required
def add_to_list(request):
    Wishlist.objects.create(
        name=request.POST['name'],
        publisher=request.POST['publisher'],
        players=request.POST['players'],
        description=request.POST['description'],
        user=request.user,
    )
    return redirect('/wishlist/')

# UPDATE


@login_required
def update(request, game_id):
    game = Game.objects.get(id=game_id)
    game.name = request.POST['name']
    game.publisher = request.POST['publisher']
    game.players = request.POST['players']
    game.description = request.POST['description']
    game.save()
    return redirect('/games/')


# DELETE

@login_required
def delete(request, game_id):
    game = Game.objects.get(id=game_id)
    game.delete()
    return redirect('/games/')


def delete_from_wishlist(request, item_id):
    item = Wishlist.objects.get(id=item_id)
    item.delete()
    return redirect('/wishlist/')


# LOGIN

def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
