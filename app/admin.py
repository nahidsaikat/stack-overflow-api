from django.contrib import admin
from .models import ClientRequestLog


class ClientRequestLogAdmin(admin.ModelAdmin):
    list_display = ['identity', 'created_at']


admin.site.register(ClientRequestLog, ClientRequestLogAdmin)
