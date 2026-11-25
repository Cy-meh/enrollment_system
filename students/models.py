from django.db import models


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    YEAR_CHOICES = [(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')]
    STATUS_CHOICES = [('Enrolled', 'Enrolled'), ('Pending', 'Pending'), ('Dropped', 'Dropped')]

    # Personal info
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    # Enrollment info
    course = models.CharField(max_length=100)
    year_level = models.IntegerField(choices=YEAR_CHOICES)
    section = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Enrolled')
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        middle = f" {self.middle_name[0]}." if self.middle_name else ""
        return f"{self.last_name}, {self.first_name}{middle}"

    @property
    def initials(self):
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class FamilyBackground(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='family')
    father_name = models.CharField(max_length=100, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_relationship = models.CharField(max_length=50, blank=True)
    guardian_contact = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Family of {self.student.full_name}"


class EducationalBackground(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='education')
    elementary_school = models.CharField(max_length=150, blank=True)
    elementary_year_graduated = models.CharField(max_length=4, blank=True)
    high_school = models.CharField(max_length=150, blank=True)
    high_school_year_graduated = models.CharField(max_length=4, blank=True)
    last_school_attended = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Education of {self.student.full_name}"