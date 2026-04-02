from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reports.models import Report


@login_required(login_url='/login/')
def worker_dashboard(request):
    reports = Report.objects.all().order_by('-date_submitted')

    # Filters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    ward_filter = request.GET.get('ward', '')
    priority_filter = request.GET.get('priority', '')

    if search_query:
        reports = reports.filter(tracking_number__icontains=search_query) | \
                  reports.filter(location__icontains=search_query)
    if status_filter:
        reports = reports.filter(status=status_filter)
    if category_filter:
        reports = reports.filter(category=category_filter)
    if ward_filter:
        reports = reports.filter(ward=ward_filter)
    if priority_filter:
        reports = reports.filter(priority=priority_filter)

    all_reports = Report.objects.all()
    total_reports = all_reports.count()
    received_count = all_reports.filter(status='received').count()
    in_progress_count = all_reports.filter(status='in_progress').count()
    resolved_count = all_reports.filter(status='resolved').count()

    return render(request, 'dashboard/worker_dashboard.html', {
        'reports': reports,
        'total_reports': total_reports,
        'received_count': received_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'ward_filter': ward_filter,
        'priority_filter': priority_filter,
    })


@login_required(login_url='/login/')
def manage_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        report.status = request.POST.get('status')
        report.priority = request.POST.get('priority')
        report.assigned_to = request.POST.get('assigned_to')
        report.completion_notes = request.POST.get('completion_notes')
        estimated = request.POST.get('estimated_completion')
        if estimated:
            report.estimated_completion = estimated
        report.save()
        messages.success(request, f'Report {report.tracking_number} updated successfully!')
        return redirect('worker_dashboard')

    return render(request, 'dashboard/manage_report.html', {'report': report})


@login_required(login_url='/login/')
def admin_dashboard(request):
    all_reports = Report.objects.all().order_by('-date_submitted')
    total_reports = all_reports.count()
    resolved_count = all_reports.filter(status='resolved').count()
    pending_count = all_reports.exclude(status='resolved').count()
    resolution_rate = round((resolved_count / total_reports * 100), 1) if total_reports > 0 else 0

    # Category data
    categories = ['water', 'sewage', 'roads', 'electricity', 'vandalism', 'other']
    category_labels = ['Water', 'Sewage', 'Roads', 'Electricity', 'Vandalism', 'Other']
    category_data = [all_reports.filter(category=c).count() for c in categories]

    # Status data
    status_data = [
        all_reports.filter(status='received').count(),
        all_reports.filter(status='assigned').count(),
        all_reports.filter(status='in_progress').count(),
        all_reports.filter(status='resolved').count(),
    ]

    # Ward data
    ward_data = [
        all_reports.filter(ward='warrenton').count(),
        all_reports.filter(ward='ikhutseng').count(),
        all_reports.filter(ward='stasie').count(),
        all_reports.filter(ward='warrenvale').count(),
        all_reports.filter(ward='14_streams').count(),
]


    recent_reports = all_reports[:5]

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_reports': total_reports,
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'resolution_rate': resolution_rate,
        'category_labels': category_labels,
        'category_data': category_data,
        'status_data': status_data,
        'ward_data': ward_data,
        'recent_reports': recent_reports,
        'all_reports': all_reports,
    })