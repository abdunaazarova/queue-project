from django.urls import path
from .views import (
    AdminDashboardView,
    HistoryListView,
    JoinQueueView,
    LeaveQueueView,
    MyQueueDetailView,
    QueueCreateView,
    ServeNextUserView,
    ServiceCreateView,
    ServiceListView,
)

app_name = 'queues'

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='services'),
    path('join/<int:service_id>/', JoinQueueView.as_view(), name='join_queue'),
    path('my/<int:entry_id>/', MyQueueDetailView.as_view(), name='my_queue'),
    path('leave/<int:entry_id>/', LeaveQueueView.as_view(), name='leave_queue'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/services/new/', ServiceCreateView.as_view(), name='admin_service_create'),
    path('admin/queues/new/', QueueCreateView.as_view(), name='admin_queue_create'),
    path('admin/queues/<int:queue_id>/serve-next/', ServeNextUserView.as_view(), name='serve_next'),
]
