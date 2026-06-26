from django.shortcuts import render
from .models import TechnicalCompliance


def dashboard_view(request):
    search_query = request.GET.get('search', '')

    # 1. Main filtered search table (keeps your case-insensitive search working!)
    if search_query:
        items = TechnicalCompliance.objects.filter(title__icontains=search_query).order_by('-publication_date')
    else:
        items = TechnicalCompliance.objects.all().order_by('-publication_date')

    # 2. Grab the execution timestamp of the absolute newest record added
    latest_record = TechnicalCompliance.objects.all().order_by('-added_at').first()

    if latest_record:
        # Pull ONLY records that were added in that exact same fetch batch run session
        latest_digest = TechnicalCompliance.objects.filter(added_at=latest_record.added_at).order_by(
            '-publication_date')
    else:
        latest_digest = None

    context = {
        'items': items,
        'search_query': search_query,
        'latest_digest': latest_digest,  # Passes the dynamic run session updates to the HTML layout
    }
    return render(request, 'tracker/dashboard.html', context)