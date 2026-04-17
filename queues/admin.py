from django.contrib import admin
from .models import Queue, QueueEntry, Service

admin.site.register(Service)
admin.site.register(Queue)
admin.site.register(QueueEntry)
