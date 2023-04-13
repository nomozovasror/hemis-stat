import django_filters
from .models import *
from django_filters import CharFilter


class ProductFilter(django_filters.FilterSet):
    employmentForm = django_filters.ModelChoiceFilter(
        queryset=EmploymentForm.objects.all(),
        empty_label="Ish o'rni",

    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        empty_label="Kafedra",
    )

    staffPosition = django_filters.ModelChoiceFilter(
        queryset=StaffPosition.objects.all(),
        empty_label="Lavozim",
    )
    department__faculty_id = django_filters.ModelChoiceFilter(
        queryset=Faculty.objects.all(),
        empty_label="Fakultet",
    )

    teacher_full_name = CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = Teachers
        fields = ['employmentForm', 'department', 'staffPosition', 'department__faculty_id',]


