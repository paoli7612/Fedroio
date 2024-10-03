from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'achievements/index.html')


def leaderboard(request):
    return render(request, 'achievements/leaderboard.html')