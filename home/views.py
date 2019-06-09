from django.shortcuts import render
from django.http import HttpResponse
from .textSummarizer import summarize
# Create your views here.
def index(request):
    return render(request, 'home.htm')

def get_summary(request):
    text = request.POST['data']
    results = summarize(text)
    return render(request, 'summary.htm', {'results':results})