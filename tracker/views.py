from django.shortcuts import render, redirect
from .models import TechnicalCompliance


def dashboard_view(request):
    # Import run_pipeline locally to prevent circular dependencies
    from .pipeline import run_pipeline

    if request.method == "POST" or request.GET.get('sync') == 'true' or 'keyword' in request.GET:
        keyword = request.GET.get('keyword', '').strip()

        # 1. Fetch live data and receive newly created document instances
        new_docs = run_pipeline(keyword=keyword if keyword else None)

        # 2. Store newly inserted record IDs in session memory
        request.session['latest_run_ids'] = [doc.id for doc in new_docs]

        if request.method == "POST":
            return redirect('dashboard')

    # Fetch batch records from the last run
    latest_ids = request.session.get('latest_run_ids', [])
    digest_records = TechnicalCompliance.objects.filter(id__in=latest_ids).order_by('-added_at')

    # All records for the main view
    all_documents = TechnicalCompliance.objects.all().order_by('-publication_date')

    context = {
        'all_documents': all_documents,
        'digest_records': digest_records,
        'latest_run_count': digest_records.count(),
    }

    return render(request, 'tracker/dashboard.html', context)