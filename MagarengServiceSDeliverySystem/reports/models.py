from django.db import models

# Create your models here.from django.db import models
import uuid


def generate_tracking_number():
    return 'MSRS-' + str(uuid.uuid4()).upper()[:8]


class Report(models.Model):

    CATEGORY_CHOICES = [
        ('water', 'Water'),
        ('sewage', 'Sewage'),
        ('roads', 'Roads'),
        ('electricity', 'Electricity'),
        ('vandalism', 'Vandalism'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('received', 'Received'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    WARD_CHOICES = [
    ('warrenton', 'Warrenton'),
    ('ikhutseng', 'Ikhutseng Location'),
    ('stasie', 'Stasie'),
    ('warrenvale', 'Warrenvale'),
    ('14_streams', '14 Streams'),
]
    

    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='report_photos/', blank=True, null=True)
    location = models.CharField(max_length=255)
    ward = models.CharField(max_length=20, choices=WARD_CHOICES, default='warrenton')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    resident_name = models.CharField(max_length=100)
    resident_phone = models.CharField(max_length=20)
    resident_email = models.EmailField(blank=True)
    assigned_to = models.CharField(max_length=100, blank=True)
    estimated_completion = models.DateField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.category} - {self.status}"
