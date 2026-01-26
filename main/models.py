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


class MemberDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('PCOR', 'PCOR Course (Parent/Coach/Official/Relations Course)'),
        ('CPR', 'CPR Certification'),
        ('ADDITIONAL_MANDATORY', 'Additional Mandatory Classes'),
        ('SPORTS_SAFETY', 'Basic Sports Safety and Injury Awareness'),
        ('MENTAL_HEALTH', 'Mental Health Awareness and Referral Basics'),
        ('COMPLIANCE', 'Program-Specific Compliance Training'),
    ]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='member_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text='Optional notes about this document')
    is_verified = models.BooleanField(default=False, help_text='Admin verification status')

    def __str__(self):
        return f"{self.participant.name} - {self.get_document_type_display()}"

    class Meta:
        ordering = ['-uploaded_at']


class VendorSubmission(models.Model):
    FREQUENCY_CHOICES = [
        ('ONE_TIME', 'One-time payment'),
        ('MONTHLY', 'Once a month'),
        ('WEEKLY', 'Once a week'),
        ('QUARTERLY', 'Once a quarter'),
        ('YEARLY', 'Once a year'),
        ('AS_NEEDED', 'As needed'),
    ]

    service_name = models.CharField(max_length=200, help_text='Name of the service or sales offering')
    business_name = models.CharField(max_length=200, blank=True)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    price_list = models.FileField(upload_to='vendor_price_lists/%Y/%m/%d/', help_text='Upload your price list document')
    description = models.TextField(blank=True, help_text='Optional description of your service')
    
    # Pricing and discount information
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Percentage of discount for P.E.P. members (e.g., 10.00 for 10%)')
    service_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Service price')
    overall_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Overall value of the service')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, blank=True, help_text='Frequency of service offered')
    
    # Free service section
    free_service_name = models.CharField(max_length=200, blank=True, help_text='Name of the free service (if applicable)')
    free_service_frequency = models.CharField(max_length=200, blank=True, help_text='How often the service is free (e.g., "Once per month", "One-time", "Annually")')
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False, help_text='Admin review status')
    is_approved = models.BooleanField(default=False, help_text='Admin approval status')

    def __str__(self):
        return f"{self.service_name} - {self.contact_name}"

    class Meta:
        ordering = ['-submitted_at']


class Donation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Stripe', help_text='Payment method used (Stripe, PayPal, etc.)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=200, blank=True, help_text='Payment processor transaction ID')
    notes = models.TextField(blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_donations')

    def __str__(self):
        return f"{self.donor_name} - ${self.amount} - {self.get_status_display()}"

    class Meta:
        ordering = ['-donated_at']


class FundDistribution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('DISTRIBUTED', 'Distributed'),
        ('CANCELLED', 'Cancelled'),
    ]

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='distributions', help_text='Source donation')
    vendor = models.ForeignKey(VendorSubmission, on_delete=models.CASCADE, related_name='fund_distributions', help_text='Vendor service receiving funds')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Amount to distribute to vendor')
    purpose = models.TextField(help_text='Purpose or description of this distribution')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    distributed_at = models.DateTimeField(null=True, blank=True, help_text='Date when funds were actually distributed')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_distributions')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_distributions')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} to {self.vendor.service_name} from {self.donation.donor_name}"

    class Meta:
        ordering = ['-created_at']


class DataVaultItem(models.Model):
    CATEGORY_CHOICES = [
        ('CERTIFICATE', 'Certificate'),
        ('DOCUMENT', 'Document'),
        ('CONTRACT', 'Contract'),
        ('LICENSE', 'License'),
        ('INSURANCE', 'Insurance'),
        ('TAX', 'Tax Document'),
        ('LEGAL', 'Legal Document'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200, help_text='Name or title of the item')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='DOCUMENT')
    description = models.TextField(blank=True, help_text='Description or notes about this item')
    file = models.FileField(upload_to='data_vault/%Y/%m/%d/', help_text='Upload the certificate or document')
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name='vault_items', help_text='Associated participant (if applicable)')
    vendor = models.ForeignKey(VendorSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name='vault_items', help_text='Associated vendor (if applicable)')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags for easy searching')
    is_encrypted = models.BooleanField(default=False, help_text='Mark if this item contains sensitive data')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_vault_items')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Expiration date (if applicable)')
    last_accessed = models.DateTimeField(null=True, blank=True, help_text='Last time this item was accessed')
    access_count = models.IntegerField(default=0, help_text='Number of times this item has been accessed')

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Data Vault Item'
        verbose_name_plural = 'Data Vault Items'
