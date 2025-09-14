from django.shortcuts import render
from data import *


def main_page(request):
    return render(request, 'main_page_app/index.html', {'specialties': specialties, 'companies': companies})
