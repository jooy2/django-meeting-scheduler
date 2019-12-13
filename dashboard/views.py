import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import MeetingAddForm, RegisterForm, CommentForm
from .models import Meeting, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime

User = get_user_model()


class MainView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        form = MeetingAddForm

        return render(request, 'main.html', {
            'form': form,
            'participants': Participants.get_all_participants(),
            'schedule': MeetingSchedule.get_weekly_schedule(request),
            'schedule_all': MeetingSchedule.get_all_schedule(),
            'all_date': MeetingSchedule.get_after_7_days(),
            'comments_all': Comments.get_all_comments(),
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
        return render(request, 'meeting_detail.html', {
            'meeting': get_object_or_404(Meeting, pk=pk),
            'comment': CommentForm(),
            'contents': Meeting.objects.get(attachment_ptr_id=pk),
            'participants': Participants.get_current_participants(pk),
        })

    @staticmethod
    def post(request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        comment = CommentForm(request.POST)

        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.meet_schedule = meeting
            comment.author = request.user
            comment.save()
            return redirect('meeting_detail', pk=meeting.pk)


class MeetingEditView(View):
    @staticmethod
    def get(request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        form = MeetingAddForm(instance=meeting)
        participants = Participants.get_all_participants()
        current_participants = Participants.get_current_participants(pk)
        print(current_participants)
        return render(request, 'meeting_edit.html', {'meeting': meeting, 'form': form,
                                                     'participants': participants,
                                                     'current_participants': current_participants})

    @staticmethod
    @login_required
    def post(request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        form = MeetingAddForm(request.POST, request.FILES, instance=meeting)
        participants = Participants.get_all_participants()
        current_participants = Participants.get_current_participants(pk)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            participants = request.POST.getlist('participants')
            all_user = User.objects.values_list('id', 'nickname')

            meet_schedule = form.save(commit=False)
            meet_schedule.proponent = request.user
            for file in files:
                a = getattr(meet_schedule, file)
                os.system('chmod 777 {}'.format(a.path))
            meet_schedule.save()

            meet_schedule.participants.remove(*meet_schedule.participants.all())

            for x in participants:
                participant_id = all_user.filter(nickname=x).values_list('id', flat=True)
                for y in participant_id:
                    meet_schedule.participants.add(y)
            return redirect('main')

        return render(request, 'meeting_edit.html', {'meeting': meeting, 'form': form,
                                                     'participants': participants,
                                                     'current_participants': current_participants})


class Participants:
    @staticmethod
    def get_all_participants():
        participants_json = []

        for val in User.objects.values_list('nickname', flat=True):
            participants_json.append({'value': val})

        return participants_json

    @staticmethod
    def get_current_participants(pk):
        user = User.objects
        participants_data = Meeting.objects.filter(id=pk).values_list('participants')
        participants_json = []

        for val in user.values_list('id', 'nickname'):
            if participants_data.filter(participants=val).exists():
                nickname = user.filter(id=val[0]).values_list('nickname', flat=True)[0]
                participants_json.append({'value': nickname, 'selected': 1})
            else:
                participants_json.append({'value': val[1], 'selected': 0})

        return participants_json


class MeetingSchedule:
    @staticmethod
    def get_after_7_days():
        date_array = []
        date_now = datetime.datetime.now()

        for current_days in range(0, 7):
            current_date = date_now + datetime.timedelta(days=current_days)
            date_array.append(current_date)

        return date_array

    @staticmethod
    def get_weekly_schedule(request):
        schedule_json = {}
        date_now = datetime.datetime.now()

        for current_days in range(0, 7):
            current_date = date_now + datetime.timedelta(days=current_days)

            schedule_data = Meeting.objects.filter(
                meet_date__contains=datetime.date(current_date.year, current_date.month, current_date.day)
            )

            for data in schedule_data:
                date_over = '1' if date_now >= data.meet_date else '0'
                joined = '1' if data.participants.filter(id=request.user.id) else '0'
                progress = '1' if data.progress else '0'

                schedule_json[data.id] = ({
                    'id': data.id, 'time': data.meet_date.strftime('%p %H:%M'),
                    'date': current_date.strftime('%Y-%m-%d'),
                    'title': data.meet_title, 'time_expired': date_over,
                    'joined': joined, 'schedule_ended': progress,
                })

        return schedule_json

    @staticmethod
    def get_all_schedule():
        schedule = Meeting.objects.all().order_by('-meet_date')[:12]
        return schedule


class Comments:
    @staticmethod
    def get_all_comments():
        comments = Comment.objects.all().order_by('-id')[:6]
        return comments

    @staticmethod
    def delete(request):
        if request.method == "POST":
            comment_id = json.loads(request.body)['pk']
            comment = get_object_or_404(Comment, pk=comment_id)

            if comment.author.pk == request.user.pk:
                comment.delete()
                message = 'removed'
            else:
                message = 'fail'
        context = {'success': message}
        return HttpResponse(json.dumps(context, ensure_ascii=False), content_type='application/json')

    @staticmethod
    def modify(request):
        if request.method == "POST":
            json_data = json.loads(request.body)
            comment = get_object_or_404(Comment, pk=json_data['pk'])
            
            if comment.author.pk == request.user.pk:
                comment.text = json_data['text']
                comment.save()
                message = 'modify'
            else:
                message = 'fail'
            context = {'success': message}
            return HttpResponse(json.dumps(context, ensure_ascii=False), content_type='application/json')
