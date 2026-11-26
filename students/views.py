from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import StudentForm, FamilyForm, EducationForm
from .models import Student

staff_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='home')


def home(request):
    """Login page."""
    if request.user.is_authenticated:
        return redirect('student_list')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect('student_list')
        form.add_error(None, 'This account does not have admin access.')
    return render(request, 'students/home.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


def student_list(request, pk=None):
    """Open to everyone (view-only for guests)."""
    query = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query)
        )

    selected = None
    if pk:
        selected = get_object_or_404(
            Student.objects.select_related('family', 'education'), pk=pk
        )

    return render(request, 'students/student_list.html', {
        'students': students,
        'selected': selected,
        'query': query,
    })


@staff_required
def student_add(request):
    student_form = StudentForm(request.POST or None, prefix='s')
    family_form = FamilyForm(request.POST or None, prefix='f')
    edu_form = EducationForm(request.POST or None, prefix='e')

    if request.method == 'POST':
        if all([student_form.is_valid(), family_form.is_valid(), edu_form.is_valid()]):
            with transaction.atomic():
                student = student_form.save()
                family = family_form.save(commit=False)
                family.student = student
                family.save()
                edu = edu_form.save(commit=False)
                edu.student = student
                edu.save()
            messages.success(request, f'{student.full_name} was enrolled.')
            return redirect('student_detail', pk=student.pk)

    return render(request, 'students/student_add.html', {
        'student_form': student_form,
        'family_form': family_form,
        'edu_form': edu_form,
    })