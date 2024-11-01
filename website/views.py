from django.shortcuts import render
import spacy
import random

nlp = spacy.load("en_core_web_lg")

words = [
    "apple", "book", "cat", "dog", "elephant", "flower", "guitar", "house", "island", "jungle",
    "kangaroo", "lemon", "mountain", "notebook", "orange", "piano", "queen", "river",
    "sun", "tree", "umbrella", "violin", "window", "xylophone", "yacht", "zebra"
]

SECRET_WORD = random.choice(words)




def games_page(request):
    return render(request, 'website/game/game_page.html')