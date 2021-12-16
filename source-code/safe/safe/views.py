from django.shortcuts import render

def homepage(request):
	context = {}
	context['homepage'] = 'This is homepage.'
	return render(request, 'homepage.html', context)