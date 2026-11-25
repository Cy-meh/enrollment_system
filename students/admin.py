from django.contrib import admin
from .models import Student, FamilyBackground, EducationalBackground


class FamilyInline(admin.StackedInline):
    model = FamilyBackground


class EducationInline(admin.StackedInline):
    model = EducationalBackground


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'last_name', 'first_name', 'course', 'year_level', 'status')
    search_fields = ('student_id', 'first_name', 'last_name')
    list_filter = ('course', 'year_level', 'status')
    inlines = [FamilyInline, EducationInline]