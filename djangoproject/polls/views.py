from pprint import pprint

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


def index(request):
    recents = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_questions": recents}
    return render(request, 'polls/index.html', context)


def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {"question": question})


def results(request, question_id):
    return HttpResponse(f"you're looking at results from {question_id}")


def vote(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        render(request, 'polls/detail.html', {
            "error_msg": 'You did not select a choice to vote for',
            "question": question
        })
    else:
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
