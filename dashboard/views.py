from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import MeetingAddForm, RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
class MainView(View):
    @staticmethod
    def get(request):
        form = MeetingAddForm
        participants_data = User.objects.values_list('nickname', flat=True)
        participants_json = []

        for val in participants_data:
            if not val == request.user.nickname:
                participants_json.append({'value': val})

        return render(request, 'main.html', {'form': form, 'participants': participants_json})

    @staticmethod
    def post(request):
        form = MeetingAddForm(request.POST)

        if form.is_valid():
            meet_schedule = form.save(commit=False)

            # TODO: 폼 저장하기 전 현재 로그인 된 사용자를 proponent에 추가해야 함

            return redirect('main')


class RegisterView(View):
    @staticmethod
    def get(request):
        form = RegisterForm

        return render(request, 'registration/register.html', {'form': form})

    @staticmethod
    def post(request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            form = RegisterForm(form.errors)
            return render(request, 'registration/register.html', {'form': form})
