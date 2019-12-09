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


class MeetingEditView(View):
    @staticmethod
    def get(request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        form = MeetingAddForm(instance=meeting)
        comment = CommentForm()
        return render(request, 'meeting_edit.html', {'meeting': meeting, 'form': form, 'comment': comment})

    @staticmethod
    @login_required
    def post(request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        form = MeetingAddForm(request.POST, request.FILES, instance=meeting)
        comment = CommentForm(request.POST)
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
            print('meeting 성공')

            if participants:
                for x in participants:
                    participant_id = all_user.filter(nickname=x).values_list('id', flat=True)
                    for y in participant_id:
                        meet_schedule.participants.add(y)
            return redirect('main')
        elif comment.is_valid():
            print('comment 성공')
            comment = comment.save(commit=False)
            comment.meet_schedule = meeting
            comment.author = request.user
            comment.save()
            return redirect('meeting_detail', pk=meeting.pk)
        else:
            print('실패')
            # comment_id = request.POST.get('pk')
            # comment = Comment.objects.filter(id=comment_id).values_list(flat=True).distinct()
            # clist = list(comment)
            # print(clist[-1])
            # if clist[-1] == comment_id:
            #     comment = get_object_or_404(Comment, pk=comment_id)
            #     comment.delete()
            #     success = True
            #     message = '댓글이 삭제 되었습니다.'
            #     context = {'message': message, 'success': success}
            #     return HttpResponse(json.dumps(context))

        return render(request, 'meeting_edit.html', {'meeting': meeting, 'form': form})
