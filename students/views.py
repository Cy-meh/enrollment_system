from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Student


@login_required
def student_list(request, pk=None):
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