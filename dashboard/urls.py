from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('schedule/view/week', views.MainView.as_view(), name='schedule_view_weekly'),
    path('meeting/<int:pk>/', views.MeetingEditView.as_view(), name='meeting_edit'),
]
