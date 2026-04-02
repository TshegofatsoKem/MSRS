from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Report


def home(request):
    total_reports = Report.objects.count()
    resolved_reports = Report.objects.filter(status='resolved').count()
    return render(request, 'home.html', {
        'total_reports': total_reports,
        'resolved_reports': resolved_reports,
    })


def submit_report(request):
    selected_category = request.GET.get('category', '')

    if request.method == 'POST':
        category = request.POST.get('category')
        location = request.POST.get('location')
        ward = request.POST.get('ward')
        description = request.POST.get('description')
        resident_name = request.POST.get('resident_name')
        resident_phone = request.POST.get('resident_phone')
        resident_email = request.POST.get('resident_email')
        photo = request.FILES.get('photo')

        report = Report.objects.create(
            category=category,
            location=location,
            ward=ward,
            description=description,
            resident_name=resident_name,
            resident_phone=resident_phone,
            resident_email=resident_email,
            photo=photo,
        )

        return redirect('confirmation', tracking_number=report.tracking_number)

    return render(request, 'reports/submit_report.html', {
        'selected_category': selected_category
    })


def confirmation(request, tracking_number):
    report = get_object_or_404(Report, tracking_number=tracking_number)
    return render(request, 'reports/confirmation.html', {'report': report})


def status_check(request):
    report = None
    error = None
    tracking_number = request.GET.get('tracking', '')

    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number', '').strip().upper()
        try:
            report = Report.objects.get(tracking_number=tracking_number)
        except Report.DoesNotExist:
            error = f'No report found with tracking number "{tracking_number}". Please check and try again.'

    return render(request, 'reports/status_check.html', {
        'report': report,
        'error': error,
        'tracking_number': tracking_number,
    })