from django.shortcuts import render
from .models import TechnicalCompliance


def dashboard(request):
    # Query all records from the database and sort them by publication date (newest first)
    regulations = TechnicalCompliance.objects.all().order_by('-publication_date')

    # Send the data to the HTML template
    return render(request, 'tracker/dashboard.html', {'regulations': regulations})