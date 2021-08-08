from database.models import Broadcast_Message, Station, Unit

# from django.conf import settings
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import View
from .tasks import update_tables
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# TODO Fix this once SSL has been sorted out
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Kiosk_View(LoginRequiredMixin, View):
    def get(self, request, view_station=None):
        if not request.user.groups.filter(name="station_view").exists():
            return HttpResponse("Unauthorized. Contact system admin.")

        if view_station is not None:
            print(f"Running update_tables for station = {view_station}")
            update_tables()

            active_units = []
            oos_units = []
            personnel = []

            try:
                s = Station.objects.get(number=view_station)
                all_units = Unit.objects.filter(station=s)
                for unit in all_units:
                    if unit.status == "OS":
                        oos_units.append(unit)
                    else:
                        active_units.append(unit)

                    if unit.employee_one is not None or unit.employee_two is not None:
                        personnel.append(unit)

            except Exception:
                return HttpResponse("Station number provided is invalid")

            if s.is_active:

                print(f"view_station={view_station} is active")

                context = {
                    "view_station": view_station,
                    "view_station_name": s.name,
                    "all_units": serializers.serialize("json", list(all_units)),
                    "active_units": serializers.serialize("json", list(active_units)),
                    "personnel": serializers.serialize("json", list(personnel)),
                    "oos_units": serializers.serialize(
                        "json",
                        list(oos_units),
                    ),
                    "messages": Broadcast_Message.objects.filter(
                        station_id__in=[view_station, 1]
                    ),
                }
                return render(request, "kiosk.html", context)
            else:

                print(f"view_station={view_station} is NOT active")

                return HttpResponse(
                    "Station not active in this system. Contact the adminitrator"
                )

        else:
            context = {"station_select": Station.objects.filter(is_active=True)}
            return render(request, "kiosk_select.html", context)
