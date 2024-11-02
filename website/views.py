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

    return render(request, 'website/cemantix/game.html', {'message': message})


def games_page(request):
    return render(request, 'website/game/game_page.html')