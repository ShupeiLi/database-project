from django.shortcuts import render

def home(request):
    """
    Define home page view. Template: home.html
    
    Returns:
        home_page_view
    """
    return render(request, "homepage/home.html")