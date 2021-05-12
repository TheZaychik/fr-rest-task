from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('polls', views.polls, name='polls'),
    path('questions', views.questions, name='questions'),
    path('userpolls', views.user_polls, name='user_polls'),
    path('auth', views.auth, name='auth'),
    path('completedpolls', views.completed_polls, name='completed_polls')

]
