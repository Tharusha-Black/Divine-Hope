from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.db.utils import IntegrityError
import json
import joblib
import os
import random
from users.models import UserScore

# Define constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'ml_models')
ENG_QUIZ_FILE = 'english-quiz.json'
IQ_QUIZ_FILE = 'iq-quiz.json'
SELF_QUIZ_FILE = 'self.json'
SVM_MODEL_FILE = 'svm_model.pkl'
NUM_QUIZZES = 10

# Helper functions
def load_quiz_pool(file_name):
    with open(os.path.join(BASE_DIR, file_name), 'r') as file:
        return json.load(file)

def get_random_quizzes(quiz_pool):
    return random.sample(quiz_pool, NUM_QUIZZES)

def calculate_score(user_answers, quiz_data):
    score = 0
    for question_number, user_answer in user_answers.items():
        correct_answer = quiz_data[int(question_number) - 1]['correct_answer']
        if user_answer == correct_answer:
            score += 1
    return score

# Views
def quiz_eng(request):
    if request.method == 'POST':
        user_answers = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('question_')}
        quiz_data = load_quiz_pool(ENG_QUIZ_FILE)
        score_eng = calculate_score(user_answers, quiz_data)
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.engTest = score_eng
        user_score.save()

    quiz_iq_pool = load_quiz_pool(IQ_QUIZ_FILE)
    random_iq_quizzes = get_random_quizzes(quiz_iq_pool)
    adjusted_iq_quizzes = [{'title': 'Quiz', 'questions': [{'question': quiz['question'], 'answers': quiz['answers'], 'correct_answer': quiz['correct_answer'], 'id': quiz['id']}]} for quiz in random_iq_quizzes]
    return render(request, 'quizs/quiz2.html', {'iq_quiz': adjusted_iq_quizzes})

def quiz_iq(request):
    if request.method == 'POST':
        user_answers = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('question_')}
        quiz_data = load_quiz_pool(IQ_QUIZ_FILE)
        score_iq = calculate_score(user_answers, quiz_data)
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.aptest = score_iq
        user_score.save()

    quiz_self_pool = load_quiz_pool(SELF_QUIZ_FILE)
    random_self_quizzes = get_random_quizzes(quiz_self_pool)
    adjusted_self_quizzes = [{'title': 'Quiz', 'questions': [{'question': quiz['question'], 'answers': quiz['answers'], 'correct_answer': quiz['correct_answer'], 'id': quiz['id']}]} for quiz in random_self_quizzes]
    return render(request, 'quizs/quiz3.html', {'self_quiz': adjusted_self_quizzes})

def quiz_self(request):
    if request.method == 'POST':
        user_answers = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('question_')}
        quiz_data = load_quiz_pool(SELF_QUIZ_FILE)
        score_self = calculate_score(user_answers, quiz_data)
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.selfTest = score_self
        user_score.save()

    if request.user.is_authenticated:
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = None
    else:
        user_score = None
    context = {'user_score': user_score}

    total = user_score.engTest + user_score.selfTest + user_score.aptest if user_score else None
    minc = 0
    if user_score.engTest < user_score.aptest and user_score.engTest < user_score.selfTest:
        minc = 1
    elif user_score.aptest < user_score.engTest and user_score.aptest < user_score.selfTest:
        minc = 2
    else:
        minc = 3

    user_score.total = total if total else 0
    user_score.low = minc
    user_score.save()  

    return render(request, 'quizs/result.html', context)

def random_quizzes_view(request):
    quiz_eng_pool = load_quiz_pool(ENG_QUIZ_FILE)
    random_eng_quizzes = get_random_quizzes(quiz_eng_pool)
    adjusted_eng_quizzes = [{'title': 'Quiz', 'questions': [{'question': quiz['question'], 'answers': quiz['answers'], 'correct_answer': quiz['correct_answer'], 'id': quiz['id']}]} for quiz in random_eng_quizzes]
    return render(request, 'quizs/quiz.html', {'eng_quiz': adjusted_eng_quizzes})

def generate_model(request):
    svm_model = joblib.load(os.path.join(MODEL_DIR, SVM_MODEL_FILE))
    if request.user.is_authenticated:
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = None
    else:
        user_score = None

    input_data = [user_score.engTest,  user_score.aptest, user_score.selfTest, user_score.total, user_score.low] if user_score else [0, 0, 0, 0, 0]
    prediction = svm_model.predict([input_data])[0] if svm_model else None

    context = {'prediction': prediction}
    return render(request, 'quizs/ss.html', context)
