from django.shortcuts import render, redirect
import json, joblib, os, random
from django.http import JsonResponse
from django.contrib import messages
from users.models import UserScore
from django.db.utils import IntegrityError


def get_eng_quiz_pool():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the JSON file
    json_file_path = os.path.join(base_dir, 'english-quiz.json')

    with open(json_file_path, 'r') as file:
        quiz_pool = json.load(file)
    return quiz_pool


def get_iq_quiz_pool():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the JSON file
    json_file_path = os.path.join(base_dir, 'iq-quiz.json')

    with open(json_file_path, 'r') as file:
        quiz_pool = json.load(file)
    return quiz_pool


def get_self_quiz_pool():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the JSON file
    json_file_path = os.path.join(base_dir, 'self.json')

    with open(json_file_path, 'r') as file:
        quiz_pool = json.load(file)
    return quiz_pool

#-----------------------------------------------------------#


def get_random_quizzes(quiz_pool, num_quizzes=10):
    return random.sample(quiz_pool, num_quizzes)


def quiz_eng(request):
    if request.method == 'POST':
        user_answers = {}
        quiz_data = get_eng_quiz_pool()
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_number = key.split('_')[1]
                user_answers[question_number] = value
        # Calculate the score

        score_eng = calculate_score(user_answers, quiz_data)
        print(f"score eng: {score_eng}")
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.engTest = score_eng
        user_score.save()

    quiz_iq_pool = get_iq_quiz_pool()
    random_iq_quizzes = get_random_quizzes(quiz_iq_pool, num_quizzes=10)
    adjusted_iq_quizzes = []
    for quiz in random_iq_quizzes:
        adjusted_quiz = {
            'title': 'Quiz',  # You can customize the title as needed
            'questions': [
                {
                    'question': quiz['question'],
                    'answers': quiz['answers'],
                    'correct_answer': quiz['correct_answer'],
                    'id': quiz['id'],
                }
            ]
        }
        adjusted_iq_quizzes.append(adjusted_quiz)
        context = {
            'iq_quiz': adjusted_iq_quizzes

        }
    return render(request, 'quizs/quiz2.html', context)


def quiz_iq(request):
    if request.method == 'POST':
        user_answers = {}
        quiz_data = get_iq_quiz_pool()
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_number = key.split('_')[1]
                user_answers[question_number] = value
        # Calculate the score
        score_iq = calculate_score(user_answers, quiz_data)
        print(f"score eng: {score_iq}")
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.aptest = score_iq
        user_score.save()

    quiz_self_pool = get_self_quiz_pool()
    random_self_quizzes = get_random_quizzes(quiz_self_pool, num_quizzes=10)
    adjusted_self_quizzes = []
    for quiz in random_self_quizzes:
        adjusted_quiz = {
            'title': 'Quiz',  # You can customize the title as needed
            'questions': [
                {
                    'question': quiz['question'],
                    'answers': quiz['answers'],
                    'correct_answer': quiz['correct_answer'],
                    'id': quiz['id'],
                }
            ]
        }
        adjusted_self_quizzes.append(adjusted_quiz)
        context = {
            'self_quiz': adjusted_self_quizzes

        }
    return render(request, 'quizs/quiz3.html', context)


def quiz_self(request):
    if request.method == 'POST':
        user_answers = {}
        quiz_data = get_self_quiz_pool()
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_number = key.split('_')[1]
                user_answers[question_number] = value
        # Calculate the score

        score_self = calculate_score(user_answers, quiz_data)
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = UserScore(users=request.user)
        user_score.selfTest = score_self
        user_score.save()
    # Assuming you want to retrieve the UserScore for the currently logged-in user
    if request.user.is_authenticated:
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = None
    else:
        user_score = None
    context = {
        'user_score': user_score
    }

    total = user_score.engTest + user_score.selfTest + user_score.aptest
    minc = 0
    if user_score.engTest < user_score.aptest and user_score.engTest < user_score.selfTest:
        minc = 1
    elif user_score.aptest < user_score.engTest and user_score.aptest < user_score.selfTest:
        minc = 2
    else:
        minc = 3

    try:
        user_score = UserScore.objects.get(users=request.user)
    except UserScore.DoesNotExist:
        user_score = UserScore(users=request.user)
    user_score.total = total
    user_score.low = minc
    user_score.save()  

    return render(request, 'quizs/result.html', context)


def random_quizzes_view(request):
    # Read the quiz pool from the JSON file
    quiz_eng_pool = get_eng_quiz_pool()

    # Randomly select 10 quizzes
    random_eng_quizzes = get_random_quizzes(quiz_eng_pool, num_quizzes=10)

    # Adjust the JSON structure to match the template's expectations
    adjusted_eng_quizzes = []
    for quiz in random_eng_quizzes:
        adjusted_quiz = {
            'title': 'Quiz',  # You can customize the title as needed
            'questions': [
                {
                    'question': quiz['question'],
                    'answers': quiz['answers'],
                    'correct_answer': quiz['correct_answer'],
                    'id': quiz['id'],
                }
            ]
        }
        adjusted_eng_quizzes.append(adjusted_quiz)

    context = {
        'eng_quiz': adjusted_eng_quizzes,
    }

    return render(request, 'quizs/quiz.html', context)

def generate_model(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to your ml_models folder and the SVM model file
    model_dir = os.path.join(base_dir, 'ml_models')
    model_file = os.path.join(model_dir, 'svm_model.pkl')
    svm_model = joblib.load(model_file)
    if request.user.is_authenticated:
        try:
            user_score = UserScore.objects.get(users=request.user)
        except UserScore.DoesNotExist:
            user_score = None
    else:
        user_score = None

    input_data = [user_score.engTest,  user_score.aptest, user_score.selfTest, user_score.total, user_score.low]  # Replace with your actual input data
    print(f"score eng: {user_score.engTest, user_score.selfTest, user_score.aptest, user_score.total, user_score.low}")
    # Make predictions using the SVM model
    prediction = svm_model.predict([input_data])

    # Process the prediction and return it to the user
    context = {
        'prediction': prediction[0],  # Assuming you have a template to display the prediction
    }

    return render(request, 'quizs/ss.html', context)

def calculate_score(user_answers, quiz_data):
    score = 0
    for question_number, user_answer in user_answers.items():
        correct_answer = quiz_data[int(question_number) - 1]['correct_answer']
        if user_answer == correct_answer:
            score += 1

    return score
