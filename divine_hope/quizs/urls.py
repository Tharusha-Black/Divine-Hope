from django.urls import path
from . import views 

urlpatterns = [
    path('random_quizzes_view/', views.random_quizzes_view, name='random_quizzes_view'),
    path('quiz_eng/', views.quiz_eng, name='quiz_eng'),
    path('quiz_iq/', views.quiz_iq, name='quiz_iq'),
    path('quiz_self/', views.quiz_self, name='quiz_self'),
    path('generate_model/', views.generate_model, name='generate_model'),
    
    
]