from django.contrib import admin
from .models import (
    Program, Participant, Document, Course, Quiz, QuizQuestion,
    Video, Test, TestQuestion, Certification, MemberDocument,
    VendorSubmission, Donation, FundDistribution, DataVaultItem
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
    list_display = ['title', 'category', 'has_google_notes', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'category', 'content', 'google_notes_url')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    def has_google_notes(self, obj):
        return bool(obj.google_notes_url)
    has_google_notes.boolean = True
    has_google_notes.short_description = 'Has Google Notes'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration', 'has_google_notes', 'created_by', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['title', 'description', 'content']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'level', 'duration', 'content', 'google_notes_url')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    def has_google_notes(self, obj):
        return bool(obj.google_notes_url)
    has_google_notes.boolean = True
    has_google_notes.short_description = 'Has Google Notes'


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
    list_display = ['title', 'validity_period', 'associated_course', 'alison_course_link', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'requirements']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Certification Information', {
            'fields': ('title', 'description', 'requirements', 'validity_period', 'associated_course')
        }),
        ('Alison Integration', {
            'fields': ('alison_course_url', 'alison_course_id'),
            'description': 'Optional: Link this certification to an Alison online course.'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']

    def alison_course_link(self, obj):
        if obj.alison_course_url:
            return obj.alison_course_url
        return ''
    alison_course_link.short_description = 'Alison URL'


@admin.register(MemberDocument)
class MemberDocumentAdmin(admin.ModelAdmin):
    list_display = ['participant', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['participant__name', 'participant__email', 'notes']
    date_hierarchy = 'uploaded_at'


@admin.register(VendorSubmission)
class VendorSubmissionAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'business_name', 'contact_name', 'email', 'is_approved', 'submitted_at']
    list_filter = ['is_reviewed', 'is_approved', 'submitted_at', 'frequency']
    search_fields = ['service_name', 'business_name', 'contact_name', 'email', 'description']
    date_hierarchy = 'submitted_at'
    readonly_fields = ['submitted_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'donor_email', 'amount', 'status', 'payment_method', 'donated_at']
    list_filter = ['status', 'payment_method', 'donated_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id', 'notes']
    date_hierarchy = 'donated_at'
    readonly_fields = ['donated_at']
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email')
        }),
        ('Donation Details', {
            'fields': ('amount', 'payment_method', 'status', 'transaction_id', 'donated_at')
        }),
        ('Additional Information', {
            'fields': ('notes', 'processed_by')
        }),
    )


@admin.register(FundDistribution)
class FundDistributionAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'donation', 'amount', 'status', 'created_by', 'created_at', 'distributed_at']
    list_filter = ['status', 'created_at', 'distributed_at']
    search_fields = ['vendor__service_name', 'vendor__contact_name', 'donation__donor_name', 'purpose', 'notes']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    fieldsets = (
        ('Distribution Details', {
            'fields': ('donation', 'vendor', 'amount', 'purpose', 'status')
        }),
        ('Timing', {
            'fields': ('created_at', 'distributed_at')
        }),
        ('Administration', {
            'fields': ('created_by', 'approved_by', 'notes')
        }),
    )


@admin.register(DataVaultItem)
class DataVaultItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'participant', 'vendor', 'uploaded_by', 'uploaded_at', 'expires_at', 'access_count']
    list_filter = ['category', 'is_encrypted', 'uploaded_at', 'expires_at']
    search_fields = ['title', 'description', 'tags', 'participant__name', 'vendor__service_name']
    date_hierarchy = 'uploaded_at'
    readonly_fields = ['uploaded_at', 'last_accessed', 'access_count', 'uploaded_by']
    fieldsets = (
        ('Item Information', {
            'fields': ('title', 'category', 'description', 'file', 'tags', 'is_encrypted')
        }),
        ('Associations', {
            'fields': ('participant', 'vendor')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'expires_at', 'last_accessed', 'access_count')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
