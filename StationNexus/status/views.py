import os
import psutil
from django.shortcuts import render, redirect
from django.views.generic import View
from database.models import Station
from django.http import HttpResponse
from redis import Redis
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from background_task import __version__ as bgt_version


class Status_View(LoginRequiredMixin, View):
    def get(self, request, action=None):
        if not request.user.groups.filter(name="server_admin").exists():
            return HttpResponse("Unauthorized. Contact system admin.")

        actions = {
            "station_load": self.station_load,
            "station_reload": self.station_reload,
            "active_station_load": self.active_station_load,
            "active_station_reload": self.active_station_reload,
            "redis_restart": self.redis_restart,
            "background_tasks_restart": self.background_tasks_restart,
        }

        if action is not None:
            actions[action]()
            return redirect("status")
        station_count = len(Station.objects.all())
        active_station_count = len(Station.objects.filter(is_active=True))

        context = {
            "redis_status": "Running" if self.redis_check() else "Stopped",
            "redis_version": self.redis_version(),
            "background_tasks_status": self.background_tasks_status(),
            "background_tasks_version": self.background_tasks_version(),
            "station_count": station_count,
            "active_station_count": active_station_count,
        }
        return render(request, "status.html", context)

    def redis_check(self):
        r = Redis(host="localhost", port=6379, socket_connect_timeout=1)
        try:
            r.ping()
            return True
        except Exception:
            return False

    def redis_version(self):
        if self.redis_check():
            r = Redis(host="localhost", port=6379, db=0)
            return r.execute_command("INFO")["redis_version"]
        else:
            return "Redis not running"

    def redis_restart(self):
        os.system("sudo systemctl restart redis-server")
        print("redis restart")

    def background_tasks_status(self):
        pstat = "Stopped"
        for proc in psutil.process_iter(["pid", "name", "cmdline", "status"]):
            if "process_tasks" in proc.info["cmdline"]:
                pstat = proc.info["status"]
        return pstat

    def background_tasks_version(self):
        return bgt_version

    def background_tasks_restart(self):
        os.system("sudo systemctl restart backround_tasks")
        print("background tasks restart")

    def station_load(self):
        with open(f"{settings.DATAFILES_DIR}/stations.csv", "r") as f:
            line = f.readline().strip("\n")
            while line:
                data = line.split(",")
                print(data[1].strip("\n"))
                Station(id=data[0], number=data[0], name=data[1].strip("\n")).save()
                line = f.readline()

    def station_reload(self):
        pass

    def active_station_load(self):
        Station.objects.filter(number=249).update(is_active=True)
        Station.objects.filter(number=266).update(is_active=True)
        Station.objects.filter(number=254).update(is_active=True)
        Station.objects.filter(number=267).update(is_active=True)

    def active_station_reload(self):
        Station.objects.filter(is_active=True).update(is_active=False)
