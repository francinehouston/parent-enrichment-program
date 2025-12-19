from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    children_ages = models.CharField(max_length=200)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-registered_at']


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    duration = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class QuizQuestion(models.Model):
    quiz = models.ForeignKey('Quiz', related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200, blank=True)
    option_4 = models.CharField(max_length=200, blank=True)
    correct_answer = models.IntegerField(default=1, help_text='1-4 for which option is correct')

    def __str__(self):
        return f"{self.quiz.title} - {self.question[:50]}"


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Quizzes'


class TestQuestion(models.Model):
    test = models.ForeignKey('Test', related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200, blank=True)
    option_4 = models.CharField(max_length=200, blank=True)
    correct_answer = models.IntegerField(default=1, help_text='1-4 for which option is correct')
    points = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.test.title} - {self.question[:50]}"


class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_limit = models.CharField(max_length=50, blank=True)
    passing_score = models.IntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def total_points(self):
        return sum(q.points for q in self.questions.all())

    class Meta:
        ordering = ['-created_at']


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Education', 'Education'),
        ('Training', 'Training'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    duration = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Certification(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    validity_period = models.CharField(max_length=100, blank=True)
    associated_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
