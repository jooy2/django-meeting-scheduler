from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('schedule/view/week', views.MainView.as_view(), name='schedule_view_weekly')
]
