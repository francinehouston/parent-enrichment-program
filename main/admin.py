from django.contrib import admin
from .models import (
    Program, Participant, Document, Course, Quiz, QuizQuestion,
    Video, Test, TestQuestion, Certification
)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'location', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created_at'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'registered_at']
    list_filter = ['registered_at']
    search_fields = ['name', 'email', 'phone']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration', 'created_by', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['title', 'description', 'content']
    date_hierarchy = 'created_at'


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = ['question', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [QuizQuestionInline]
    date_hierarchy = 'created_at'


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1
    fields = ['question', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer', 'points']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'passing_score', 'time_limit', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [TestQuestionInline]
    date_hierarchy = 'created_at'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'validity_period', 'associated_course', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'requirements']
    date_hierarchy = 'created_at'
