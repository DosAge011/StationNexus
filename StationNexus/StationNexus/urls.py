"""StationNexus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from status.views import Status_View
from kiosk.views import Kiosk_View
from authentication.views import Login_View, Logout_View
from status.tasks import bg_tasks_status
from kiosk.tasks import bg_tasks_station_update, update_tables
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("status/", Status_View.as_view(), name="status"),
    path("status/<action>", Status_View.as_view(), name="status"),
    path("login/", Login_View.as_view(), name="login"),
    path("logout/", Logout_View.as_view(), name="logout"),
    path("kiosk/", Kiosk_View.as_view(), name="kiosk"),
    path("kiosk/<view_station>/", Kiosk_View.as_view(), name="kiosk"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


bg_tasks_status(repeat=10, repeat_until=None)

bg_tasks_station_update(repeat=10, repeat_until=None)
update_tables()
update_tables(repeat=10, repeat_until=None)
