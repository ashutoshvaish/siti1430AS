from django.shortcuts import render, get_object_or_404
from dal import autocomplete
from .models import Fees, Student


def home(request):
    return render(request, 'home.html')

def print_fee_slip(request, pk):
    fee = get_object_or_404(Fees, pk=pk)
    return render(request, 'fee_slip.html', {'fee': fee})


class StudentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Student.objects.none()

        qs = Student.objects.all()

        # Get the search term and filter by name or roll_no
        if self.q:
            qs = qs.filter(
                student_name__icontains=self.q
            ) | qs.filter(
                roll_no__icontains=self.q
            )

        return qs
