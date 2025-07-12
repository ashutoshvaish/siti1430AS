from django.urls import path
from . import views
from .views import StudentAutocomplete


urlpatterns = [
    path('', views.home, name='home'),
    path('print-slip/<int:pk>/', views.print_fee_slip, name='print_fee_slip'),
    path('student-autocomplete/', StudentAutocomplete.as_view(), name='student-autocomplete'),
]
