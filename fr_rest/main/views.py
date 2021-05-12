from datetime import datetime, timezone
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main import models
from main import serializers
from main import subfunctions


@api_view(['POST', 'PATCH', 'DELETE', 'GET'])
@login_required()
def polls(request):
    poll_serializer = serializers.PollSerializer(data=request.data)
    if not poll_serializer.is_valid():
        return Response(poll_serializer.errors, status=400)
    if request.method == 'POST':
        err = poll_serializer.create(request.data)
        if err != 0:
            return Response(err.__str__(), status=400)
        return Response(status=201)
    elif request.method == 'PATCH':
        poll = subfunctions.get_poll_or_none_by_name(request.data['name'])
        if poll is None:
            return Response('Object not found', status=400)
        err = poll_serializer.update(poll, request.data)
        if err != 0:
            return Response(err.__str__(), status=400)
        return Response(status=200)
    elif request.method == 'GET':
        polls = models.Poll.objects.all()
        polls_questions = []
        for p in polls:
            polls_questions.append({
                'poll_id': p.id,
                'name': p.name,
                'start_date': p.start_date,
                'end_date': p.end_date,
                'description': p.description,
                'questions': subfunctions.get_questions_for_polls(p.id)
            })
        return Response(polls_questions, status=200)
    else:
        poll = subfunctions.get_poll_or_none_by_name(request.data['name'])
        if poll is None:
            return Response('Object not found', status=400)
        poll.delete()
        return Response(status=200)


@api_view(['POST', 'PATCH', 'DELETE'])
def questions(request):
    questions_serializer = serializers.QuestionSerializer(data=request.data)
    if not questions_serializer.is_valid():
        return Response(questions_serializer.errors, status=400)
    if request.method == 'POST':
        err = questions_serializer.create(request.data)
        if err != 0:
            return Response(err.__str__(), status=400)
        return Response(status=201)
    elif request.method == 'PATCH':
        question = subfunctions.get_question_or_none_by_question(request.data['question'])
        if question is None:
            return Response('Object not found', status=400)
        err = questions_serializer.update(question, request.data)
        if err != 0:
            return Response(err.__str__(), status=400)
        return Response(status=200)
    else:
        question = subfunctions.get_question_or_none_by_question(request.data['question'])
        if question is None:
            return Response('Object not found', status=400)
        question.delete()
        return Response(status=200)


@api_view(['POST', 'GET'])
def auth(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        if user.check_password(password):
            login(request, user)
            return Response(status=200)
        else:
            return Response(status=403)
    else:
        logout(request)
        return Response(status=200)


@api_view(['POST', 'GET'])
def user_polls(request):
    if request.method == 'GET':
        polls = models.Poll.objects.all()
        polls_questions = []
        for p in polls:
            if p.start_date < datetime.now(tz=timezone.utc) < p.end_date:
                polls_questions.append({
                    'poll_id': p.id,
                    'name': p.name,
                    'start_date': p.start_date,
                    'end_date': p.end_date,
                    'description': p.description,
                    'questions': subfunctions.get_questions_for_polls(p.id)
                })
        return Response(polls_questions, status=200)
    else:
        if not (request.data.get('user_id') and request.data.get('polls')):
            return Response(status=400)
        cUser = subfunctions.get_c_user_or_none_by_id(request.data.get('user_id'))
        if not cUser:
            cUser = models.CUser(user_id=request.data.get('user_id'))
            cUser.competed_polls = []
        polls = request.data['polls']
        for p in polls:
            if not p['poll_id'] in cUser.competed_polls:
                cUser.competed_polls.append(p)
        cUser.save()
        return Response(status=200)


@api_view(['POST'])
def completed_polls(request):
    if not request.data.get('user_id'):
        return Response(status=400)
    cUser = subfunctions.get_c_user_or_none_by_id(request.data.get('user_id'))
    if not cUser:
        return Response(status=400)
    return Response(cUser.competed_polls, status=200)
