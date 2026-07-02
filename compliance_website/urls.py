from django.contrib import admin
from django.urls import path
from tracker import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('fetch-live-data/', views.fetch_live_data, name='fetch_live_data'),
    path('document/<int:pk>/', views.document_detail_view, name='document_detail'),
]
