from django.contrib import admin
from .models import Report
# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'category', 'status', 'priority', 'ward', 'resident_name', 'date_submitted']
    list_filter = ['status', 'category', 'priority', 'ward']
    search_fields = ['tracking_number', 'resident_name', 'location']
    readonly_fields = ['tracking_number', 'date_submitted', 'date_updated']