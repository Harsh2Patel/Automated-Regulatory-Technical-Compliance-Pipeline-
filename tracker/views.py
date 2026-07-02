from django.shortcuts import render, redirect
from .models import TechnicalCompliance
from .pipeline import run_federal_register_pipeline


def dashboard_view(request):
    items = TechnicalCompliance.objects.all().order_by('-publication_date')

    # 1. Find the exact timestamp of the absolute newest record added
    latest_record = TechnicalCompliance.objects.all().order_by('-added_at').first()

    if latest_record:
        # 2. ONLY show records that share that exact same fetch session timestamp
        latest_digest = TechnicalCompliance.objects.filter(added_at=latest_record.added_at)
    else:
        latest_digest = TechnicalCompliance.objects.none()

    context = {
        'items': items,
        'latest_digest': latest_digest
    }
    return render(request, 'tracker/dashboard.html', context)


def fetch_live_data(request):
    if request.method == "POST":
        raw_keywords = request.POST.get('custom_keywords', '')

        if raw_keywords.strip():
            keyword_list = [kw.strip().lower() for kw in raw_keywords.split(',') if kw.strip()]
        else:
            keyword_list = ['safety', 'coast guard', 'environmental']

        run_federal_register_pipeline(keyword_list)
        return redirect('/?tab=digest')

    return redirect('/')


def document_detail_view(request, pk):
    document = TechnicalCompliance.objects.get(pk=pk)
    context = {
        'document': document
    }
    return render(request, 'tracker/document_detail.html', context)