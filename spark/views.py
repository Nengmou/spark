from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

# import pyRserve
import json

from spark.models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'common/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'common/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'common/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'common/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('spark:results', args=(p.id,)))


def opt(request):
    # conn = pyRserve.connect()
    # conn.eval('rm(list=ls())')
    # conn.r.input_total_amt = int(request.GET['budget'])
    # res2 = conn.eval("source('C:/Users/yixiang/Desktop/opt_total.R')")
    # result = json.loads(res2['value'])
    # conn.close()
    # return HttpResponse(json.dumps(result), content_type='application/json')
    return HttpResponse(json.dumps('sample data'), content_type='application/json')
