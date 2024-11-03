from django.shortcuts import render
from website.models import Guess
import spacy
import random

nlp = spacy.load("en_core_web_lg")

words = [
    "apple", "book", "cat", "dog", "elephant", "flower", "guitar", "house", "island", "jungle"
]

SECRET_WORD = random.choice(words)
token_secret_word = nlp(SECRET_WORD)

def cemantix_game(request):
    message = ""
    if request.method == "POST":
        given_word = request.POST.get('word') # retrieves the value form
        if given_word:
            token_given_word = nlp(given_word)
            similarity = token_given_word.similarity(token_secret_word)
            similarity = round(similarity * 100, 2)

            Guess.objects.create(word=given_word, similarity=similarity) # save in bdd

            message = f"Your word '{given_word}' has a similarity of {similarity}% with the secret word."

            if similarity == 100:
                cemantix_change_word(similarity)
                message += f"GG! You've found the secret word '{given_word}'. A new secret word has been set."

    return render(request, 'website/cemantix/game.html', {'message': message})

def cemantix_change_word(similarity):
    global SECRET_WORD, token_secret_word
    if similarity == 100:
        SECRET_WORD = random.choice(words)
        token_secret_word = nlp(SECRET_WORD)

def games_page(request):
    return render(request, 'website/game/game_page.html')