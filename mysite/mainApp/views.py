
from django.shortcuts import render

def index(request):
    return render(request, 'mainApp/cur.html')
# Create your views here.
