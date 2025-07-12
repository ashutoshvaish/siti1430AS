from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.shortcuts import render
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.db.models import Sum, F, Value
from django.db.models.functions import ExtractYear, Coalesce
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import Student, Fees
from .forms import FeesForm

# -------------------------
# Custom Filter for Admission Year
# -------------------------
class AdmissionYearFilter(admin.SimpleListFilter):
    title = _('Admission Year')
    parameter_name = 'admission_year'

    def lookups(self, request, model_admin):
        years = Student.objects.dates('date_of_admission', 'year')
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date_of_admission__year=self.value())
        return queryset

# -------------------------
# Student Resource for Import/Export
# -------------------------
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

# -------------------------
# Student Admin
# -------------------------
@admin.register(Student)
class StudentAdmin(ExtraButtonsMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('student_name', 'father_name', 'roll_no', 'batch_year_display', 'trade', 'mobile_no', 'total_fees', 'fees_paid', 'pending_fees')
    search_fields = ('student_name', 'father_name', 'roll_no', 'trade', 'mobile_no')
    list_filter = ('trade', AdmissionYearFilter,)

    def batch_year_display(self, obj):
        return obj.batch_year
    batch_year_display.short_description = 'Batch Year'

    # -------------------------
    # Batch Summary Button
    # -------------------------
    @button(name='batch_summary', label='Batch-wise Summary', html_attrs={'class': 'button'})
    def batch_summary(self, request):
        batches = (
            Student.objects
            .annotate(year=ExtractYear('date_of_admission'))
            .values('year')
            .annotate(total_estimated_fees=Coalesce(Sum('total_fees'), Value(0)))
            .order_by('-year')
        )
        batches = list(batches)

        batches2 = (
            Student.objects
            .annotate(year=ExtractYear('date_of_admission'))
            .values('year')
            .annotate(total_collected=Coalesce(Sum('fees__amount'), Value(0)))
            .order_by('-year')
        )
        batches2 = list(batches2)

        collected_dict = {item['year']: item['total_collected'] for item in batches2}

        merged_batches = []
        for item in batches:
            year = item['year']
            total_collected = collected_dict.get(year, 0)
            total_pending = item['total_estimated_fees'] - total_collected

            merged_batches.append({
                'year': year,
                'total_estimated_fees': item['total_estimated_fees'],
                'total_collected': total_collected,
                'total_pending': total_pending
            })

        context = dict(
            self.admin_site.each_context(request),
            batches=merged_batches,
        )

        return render(request, 'batch_summary.html', context)

# -------------------------
# Fees Resource for Import/Export
# -------------------------
class FeesResource(resources.ModelResource):
    class Meta:
        model = Fees

# -------------------------
# Fees Admin
# -------------------------
@admin.register(Fees)
class FeesAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    form = FeesForm
    search_fields = ('student__student_name', 'student__roll_no', 'fees_receipt_no',)
    list_display = ('student', 'amount', 'date', 'payment_mode', 'collected_by', 'print_slip_link')
    readonly_fields = ('collected_by',)
    list_filter = (('date', admin.DateFieldListFilter),)

    def print_slip_link(self, obj):
        url = reverse('print_fee_slip', args=[obj.pk])
        return format_html(f'<a class="button" href="{url}" target="_blank">Print Fee Slip</a>')
    print_slip_link.short_description = 'Print Fee Slip'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New record
            obj.collected_by = request.user
        super().save_model(request, obj, form, change)
