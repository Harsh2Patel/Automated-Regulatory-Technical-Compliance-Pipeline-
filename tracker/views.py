from django.shortcuts import render
from .models import TechnicalCompliance


def dashboard_view(request):
    # 1. Get the search query from the URL (defaults to empty string if not found)
    search_query = request.GET.get('search', '')

    # 2. Fetch compliance items from the database
    if search_query:
        # Filters titles containing the search query (case-insensitive)
        items = TechnicalCompliance.objects.filter(title__icontains=search_query)
    else:
        items = TechnicalCompliance.objects.all()

    context = {
        'items': items,
        'search_query': search_query,
    }
    return render(request, 'tracker/dashboard.html', context)