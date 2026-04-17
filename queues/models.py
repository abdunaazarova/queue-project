from django.conf import settings
from django.db import models
from django.utils import timezone


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('hospital', 'Hospital'),
        ('bank', 'Bank'),
        ('government', 'Government'),
        ('school', 'School'),
        ('restaurant', 'Restaurant'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_services'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Queue(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='queue')
    estimated_wait_minutes = models.PositiveIntegerField(default=15)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='QueueEntry', related_name='queues')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_queues'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def waiting_entries(self):
        return self.entries.filter(status=QueueEntry.Status.WAITING).order_by('position')

    def total_waiting(self):
        return self.waiting_entries().count()

    def __str__(self):
        return f'Queue - {self.service.name}'


class QueueEntry(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        DONE = 'done', 'Done'
        LEFT = 'left', 'Left'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='queue_entries')
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name='entries')
    position = models.PositiveIntegerField(null=True, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.WAITING)

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f'{self.user.email} in {self.queue.service.name}'
