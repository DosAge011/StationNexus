from django.contrib import admin

from .models import Station
from .models import Broadcast_Message
from .models import Unit

admin.site.register(Station)
admin.site.register(Broadcast_Message)
admin.site.register(Unit)
