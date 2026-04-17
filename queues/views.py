from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Max, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from notifications.models import Notification
from .forms import QueueConfigForm, ServiceForm
from .models import Queue, QueueEntry, Service


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'queues/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = Service.objects.select_related('queue').filter(queue__isnull=False)
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(location__icontains=q))
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Service.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', 'all')
        return context


class JoinQueueView(LoginRequiredMixin, View):
    def post(self, request, service_id):
        queue = get_object_or_404(Queue, service_id=service_id)
        existing = QueueEntry.objects.filter(user=request.user, queue=queue, status=QueueEntry.Status.WAITING).first()
        if existing:
            messages.info(request, 'You are already in this queue.')
            return redirect('queues:my_queue', entry_id=existing.id)

        max_position = queue.entries.filter(status=QueueEntry.Status.WAITING).aggregate(Max('position'))['position__max'] or 0
        entry = QueueEntry.objects.create(user=request.user, queue=queue, position=max_position + 1)
        messages.success(request, f'You joined the queue for {queue.service.name}.')
        return redirect('queues:my_queue', entry_id=entry.id)


class MyQueueDetailView(LoginRequiredMixin, DetailView):
    model = QueueEntry
    template_name = 'queues/my_queue.html'
    context_object_name = 'entry'
    pk_url_kwarg = 'entry_id'

    def get_queryset(self):
        return QueueEntry.objects.select_related('queue__service').filter(user=self.request.user, status=QueueEntry.Status.WAITING)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object
        ahead = entry.queue.entries.filter(status=QueueEntry.Status.WAITING, position__lt=entry.position).count()
        total = entry.queue.total_waiting()
        progress = int(((total - ahead) / total) * 100) if total else 100
        estimated = ahead * entry.queue.estimated_wait_minutes
        context.update({'people_ahead': ahead, 'total_people': total, 'progress': progress, 'estimated_wait': estimated})

        if ahead == 3:
            Notification.objects.get_or_create(user=self.request.user, message='3 people ahead. Get ready!')
        if ahead == 0:
            Notification.objects.get_or_create(user=self.request.user, message="It's your turn! Please proceed to the counter.")
        return context


class LeaveQueueView(LoginRequiredMixin, View):
    def post(self, request, entry_id):
        entry = get_object_or_404(QueueEntry, id=entry_id, user=request.user, status=QueueEntry.Status.WAITING)
        queue = entry.queue
        old_position = entry.position
        entry.status = QueueEntry.Status.LEFT
        entry.completed_at = timezone.now()
        entry.position = None
        entry.save(update_fields=['status', 'completed_at', 'position'])
        queue.entries.filter(status=QueueEntry.Status.WAITING, position__gt=old_position).update(position=F('position') - 1)
        messages.warning(request, 'You have left the queue.')
        return redirect('queues:services')


class HistoryListView(LoginRequiredMixin, ListView):
    template_name = 'queues/history.html'
    context_object_name = 'history_entries'

    def get_queryset(self):
        return QueueEntry.objects.select_related('queue__service').filter(user=self.request.user).exclude(status=QueueEntry.Status.WAITING)


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'queues/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['queues'] = Queue.objects.select_related('service').all()
        context['active_entries'] = QueueEntry.objects.select_related('user', 'queue__service').filter(status=QueueEntry.Status.WAITING)
        return context


class ServiceCreateView(AdminRequiredMixin, CreateView):
    template_name = 'queues/admin_service_form.html'
    form_class = ServiceForm
    success_url = reverse_lazy('queues:admin_dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Service created successfully.')
        return super().form_valid(form)


class QueueCreateView(AdminRequiredMixin, CreateView):
    template_name = 'queues/admin_queue_form.html'
    form_class = QueueConfigForm
    success_url = reverse_lazy('queues:admin_dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Queue created successfully.')
        return super().form_valid(form)


class ServeNextUserView(AdminRequiredMixin, View):
    def post(self, request, queue_id):
        queue = get_object_or_404(Queue, id=queue_id)
        current = queue.entries.filter(status=QueueEntry.Status.WAITING).order_by('position').first()
        if not current:
            messages.info(request, 'No users waiting in this queue.')
            return redirect('queues:admin_dashboard')

        current.status = QueueEntry.Status.DONE
        current.completed_at = timezone.now()
        current.position = None
        current.save(update_fields=['status', 'completed_at', 'position'])
        queue.entries.filter(status=QueueEntry.Status.WAITING).update(position=F('position') - 1)
        Notification.objects.create(user=current.user, message=f'Queue completed for {queue.service.name}.')
        messages.success(request, f'{current.user.email} has been served.')
        return redirect('queues:admin_dashboard')
