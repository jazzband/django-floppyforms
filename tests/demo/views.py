from django.shortcuts import render

from .forms import AllFieldsForm


def index(request):
    if request.method == 'POST':
        form = AllFieldsForm(request.POST, request.FILES)
    else:
        form = AllFieldsForm()
    return render(request, 'demo/index.html', {
        'form': form,
    })
