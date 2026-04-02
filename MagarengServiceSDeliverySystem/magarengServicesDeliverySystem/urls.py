"""
URL configuration for magarengServicesDeliverySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
] """




from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reports import views as report_views
from accounts import views as account_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', report_views.home, name='home'),
    path('report/', report_views.submit_report, name='submit_report'),
    path('confirmation/<str:tracking_number>/', report_views.confirmation, name='confirmation'),
    path('status/', report_views.status_check, name='status_check'),
    path('login/', account_views.staff_login, name='login'),
    path('logout/', account_views.staff_logout, name='logout'),
    path('worker/', dashboard_views.worker_dashboard, name='worker_dashboard'),
    path('worker/report/<int:report_id>/', dashboard_views.manage_report, name='manage_report'),
    path('dashboard/admin/', dashboard_views.admin_dashboard, name='admin_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)