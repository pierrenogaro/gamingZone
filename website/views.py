from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from website.forms import SignupForm, LoginForm
from website.models import Hangman, Cemantix, Score
import spacy
import random

######################## CEMANTIX ########################

nlp = spacy.load("en_core_web_lg")

words = [
    "apple", "book", "cat", "dog", "elephant", "flower", "guitar", "house", "island", "jungle"
]

SECRET_WORD = random.choice(words)
token_secret_word = nlp(SECRET_WORD)

@login_required
def cemantix_game(request):
    message = ""
    guesses = Cemantix.objects.all()
    user_score, _ = Score.objects.get_or_create(user=request.user)

    if request.method == "POST":
        given_word = request.POST.get('word') # retrieves the value form
        if given_word:
            token_given_word = nlp(given_word)
            similarity = token_given_word.similarity(token_secret_word)
            similarity = round(similarity * 100, 2)

            Cemantix.objects.create(word=given_word, similarity=similarity) # save in bdd

            message = f"Your word '{given_word}' has a similarity of {similarity}% with the secret word."

            if similarity == 100:
                user_score.points += 10
                user_score.save()
                cemantix_change_word(similarity)
                message += " A new secret word has been set."
            else:
                user_score.points -= 1
                user_score.save()

    return render(request, 'website/cemantix/game.html', {'message': message, 'guesses': guesses})

def cemantix_change_word(similarity):
    global SECRET_WORD, token_secret_word
    if similarity == 100:
        Cemantix.objects.all().delete()
        SECRET_WORD = random.choice(words)
        token_secret_word = nlp(SECRET_WORD)

######################## HANGMAN ########################

WORDS_HANG = ["hockey", "canada", "beer", "pizza", "python"]
life_hang = 7

def hang_lose(guessed_letters):
    return len(guessed_letters) == life_hang

@login_required
def hangman_game(request):
    solution = request.POST.get('solution', random.choice(WORDS_HANG))
    guesse_letter = request.POST.get('guesse_letter', '') + request.POST.get('guess', '')
    user_score, _ = Score.objects.get_or_create(user=request.user)
    see = ''.join(
        letter + " " if letter in guesse_letter else "_ "
        for letter in solution
    )

    Hangman.objects.create(solution=solution, guesse_letter=guesse_letter)

    if "_" not in see:
        user_score.points += 5
        user_score.save()
        return render(request, 'website/hangman/win.html', {'solution': solution})

    if hang_lose(guesse_letter):
        user_score.points -= 10
        user_score.save()
        return render(request, 'website/hangman/lose.html', {'solution': solution})

    return render(request, 'website/hangman/game.html', {'see': see, 'solution': solution, 'guesse_letter': guesse_letter, 'score': user_score.points})

######################## GAMES ########################
def games_page(request):
    return render(request, 'website/game/game_page.html')

@login_required
def leaderboard(request):
    scores = Score.objects.select_related('user').order_by('-points')
    return render(request, 'website/leaderboard/index.html', {'scores': scores})

######################## REGISTRATION ########################

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'website/registration/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('games_page')
    else:
        form = LoginForm()
    return render(request, 'website/registration/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('login')