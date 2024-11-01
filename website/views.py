from django.shortcuts import render

def games_page(request):
    return render(request, 'website/game/game_page.html')