from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import MeetingAddForm, RegisterForm
from .models import Meeting
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime

User = get_user_model()


class MainView(View):
    @staticmethod
    def get(request):
        form = MeetingAddForm
        participants_data = User.objects.values_list('nickname', flat=True)
        participants_json = []
        schedule_json = {}
        date_array = []

        # get participants
        for val in participants_data:
            if not val == request.user.nickname:
                participants_json.append({'value': val})

        # get schedule 7 days
        for current_days in range(0, 7):
            current_date = datetime.datetime.now() + datetime.timedelta(days=current_days)
            current_date_format = current_date.strftime('%Y-%m-%d')
            date_array.append(current_date_format)

            schedule_data = Meeting.objects.filter(
                meet_date__contains=datetime.date(current_date.year, current_date.month, current_date.day)
            )

            for data in schedule_data:
                schedule_json[data.id] = ({'date': current_date_format, 'title': data.meet_title})

        return render(request, 'main.html', {
            'form': form,
            'participants': participants_json,
            'schedule': schedule_json,
            'date': date_array,
        })


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
