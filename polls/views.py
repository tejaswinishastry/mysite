# Create your views here.
#index shows the latest 5 polls

from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Choice, Poll
# ...
def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p,'choice_arr':choice_arr})

def vote(request, poll_id):
    global choice
    p = get_object_or_404(Poll, pk=poll_id)
    #voted_polls  = request.session.get('has_voted_poll',[])
    #if poll_id in voted_polls:
    #    return render_to_response('polls/results.html',
    #                  RequestContext(request,{
    #                                  'object': p,
    #                                  'error_message': "You have already voted.",
    #                              }))

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        p.total_votes += 1
        selected_choice.save()
        p.voted = True
        p.save()
        #request.session['has_voted_poll']=voted_polls+[poll_id]
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect('/polls/%s/results/' % poll.id)
        
        choices = list(p.choice_set.all())
        for choice in choices:
            percent = choice.votes*100/p.total_votes
            choice.percentage = percent
            choice.save()
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))
        
    #return render_to_response('polls/9/results.html',{})
            

