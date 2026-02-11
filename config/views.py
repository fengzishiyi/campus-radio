"""
Views for the campus-radio project.
"""

from django.shortcuts import render


def home_view(request):
    """
    Render the home page.
    """
    return render(request, 'home.html')
