from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import AllFieldsForm


def index(request):
    if request.method == 'POST':
        form = AllFieldsForm(request.POST, request.FILES)
    else:
        form = AllFieldsForm()
    return render_to_response('demo/index.html', {
        'form': form,
    }, context_instance=RequestContext(request))
