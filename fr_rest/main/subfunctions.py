from main import models


def get_poll_or_none_by_name(name):
    try:
        instance = models.Poll.objects.all().get(name=name)
    except Exception:
        return None
    return instance


def get_question_or_none_by_question(question):
    try:
        instance = models.Question.objects.all().get(question=question)
    except Exception:
        return None
    return instance


def get_c_user_or_none_by_id(id):
    try:
        instance = models.CUser.objects.all().get(user_id=id)
    except Exception:
        return None
    return instance


def get_questions_for_polls(poll_id):
    list_questions = []
    questions = models.Question.objects.all().filter(poll_id=poll_id)
    for q in questions:
        list_questions.append({
            'poll': q.poll_id,
            'type': q.type,
            'question': q.question,
            'answers': q.answers
        })
    return list_questions
