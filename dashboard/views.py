from django.shortcuts import render
from django.views.generic import View


class MainView(View):
    @staticmethod
    def get(request):
        return render(request, 'main.html', {})