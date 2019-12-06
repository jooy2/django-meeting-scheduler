from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import MeetingAddForm, RegisterForm
from .models import Meeting
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime

User = get_user_model()


class MainView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        form = MeetingAddForm
        participants_data = User.objects.values_list('nickname', flat=True)
        participants_json = []
        schedule_json = {}
        date_array = []
        date_now = datetime.datetime.now()

        # get participants
        for val in participants_data:
            if not val == request.user.nickname:
                participants_json.append({'value': val})
                
        # get schedule 7 days
        for current_days in range(0, 7):
            current_date = date_now + datetime.timedelta(days=current_days)
            current_date_format = current_date.strftime('%Y-%m-%d')
            date_array.append(current_date)

            schedule_data = Meeting.objects.filter(
                meet_date__contains=datetime.date(current_date.year, current_date.month, current_date.day)
            )

            for data in schedule_data:
                if date_now >= data.meet_date:
                    date_over = '1'
                else:
                    date_over = '0'

                if data.participants.filter(id=request.user.id):
                    joined = '1'
                else:
                    joined = '0'

                schedule_json[data.id] = ({
                    'id': data.id, 'time': data.meet_date.strftime('%p %H:%M'), 'date': current_date_format,
                    'title': data.meet_title, 'time_expired': date_over, 'join_stat': joined
                })

        return render(request, 'main.html', {
            'form': form,
            'participants': participants_json,
            'schedule': schedule_json,
            'all_date': date_array,
        })

    @staticmethod
    @login_required
    def post(request):
        form = MeetingAddForm(request.POST)

        if form.is_valid():
            participants = request.POST.getlist('participants')
            all_user = User.objects.values_list('id', 'nickname')

            meet_schedule = form.save(commit=False)
            meet_schedule.proponent = request.user
            meet_schedule.save()

            for x in participants:
                participant_id = all_user.filter(nickname=x).values_list('id', flat=True)
                for y in participant_id:
                    meet_schedule.participants.add(y)

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


class MeetingDetailView(View):
    @staticmethod
    def get(request, pk):
        return render(request, 'meeting_detail.html', {})
