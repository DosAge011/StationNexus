import requests
from background_task import background
from background_task.models import CompletedTask, Task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from bs4 import BeautifulSoup
from database.models import Station, Unit

from django.core import serializers
import json


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# needed to ensure the task queue is clear before adding
# and executing a new task with ./manage.py process_tasks
Task.objects.all().delete()
CompletedTask.objects.all().delete()
channel_layer = get_channel_layer()


@background(schedule=5)
def bg_tasks_station_update(*kwargs):
    active_stations = Station.objects.filter(is_active=True)
    for stn in active_stations:
        collect_data(stn.id)


@background(schedule=5)
def collect_data(station):
    collector.collect(station)


@background(schedule=5)
def update_tables(*kwargs):
    print("Updating Table Data")

    active_stations = Station.objects.filter(is_active=True)

    for stn in active_stations:
        all_units = Unit.objects.filter(station=stn)

        active_units = []
        oos_units = []
        personnel = []

        all_units = Unit.objects.filter(station=stn)
        for unit in all_units:
            if unit.status == "OS":
                oos_units.append(unit)
            else:
                active_units.append(unit)

            if unit.employee_one is not None or unit.employee_two is not None:
                personnel.append(unit)

        async_to_sync(channel_layer.group_send)(
            f"data_{stn.id}",
            {
                "type": "send_data",
                "active_units": serializers.serialize("json", list(active_units)),
                "oos_units": serializers.serialize("json", list(oos_units)),
                "personnel": serializers.serialize("json", list(personnel)),
            },
        )


# @background(schedule=5)
# def data_collect(*kwargs):
#     collector = Collector()
#     with ThreadPoolExecutor() as exe:
#         results = [
#             exe.submit(collector.collect, s.number)
#             for s in Station.objects.filter(is_active=True)
#         ]

#         for r in as_completed(results):
#             print(r.result())


class Collector:
    def __init__(self):
        with open("/etc/station_nexus.json") as f:
            values = json.load(f)
            scrape_user = values["scrape_user"]
            scrape_pass = values["scrape_pass"]

        login_data = {"username": scrape_user, "password": scrape_pass}
        login_url = "https://performance1.bcas.ca/login-process.php"
        s = requests.Session()
        s.post(login_url, data=login_data, verify=False)
        self.session = s

    def collect(self, station):
        print(f"collect called for {station}")
        stn = Station.objects.get(number=station)
        db_units = Unit.objects.filter(station=stn)
        units = self.scrape(station)

        # TODO add logic for day shift vs night shift, adding and removing cars and for
        # durations here. break into new class/file if needed

        # 1) clear all units from database that are not in the new unit list
        # 2) for units in the database that are in the new unit list
        # a) is the status the same
        # YES - Do nothing
        # NO - Update with the new status ensure datetime last change reflects the changes

        for db_unit in db_units:
            in_list = False
            for unit in units:
                if db_unit.call_sign == unit.call_sign:
                    in_list = True
                    break
            if not in_list:
                db_unit.delete()

        for u in units:
            u.station = stn
            if not Unit.objects.filter(call_sign=u.call_sign).exists():
                print(f"new car found adding ({u.call_sign}) to db")
                u.save()
            else:
                db_unit = Unit.objects.get(call_sign=u.call_sign)
                if not u.status == db_unit.status:
                    db_unit.status = u.status
                    db_unit.event_id = u.event_id
                    db_unit.event_type = u.event_type
                    db_unit.event_sub_type = u.event_sub_type
                    db_unit.location = u.location
                    db_unit.out_of_service_code = u.out_of_service_code
                    db_unit.employee_one = u.employee_one
                    db_unit.employee_two = u.employee_two
                    db_unit.unit_phone_number = u.unit_phone_number
                    db_unit.save()
        print(f"collect complete {station}")
        return f"collect complete {station}"

    def scrape(self, station):
        print(f"scraping for {station}")
        r = self.session.get(
            f"https://performance1.bcas.ca/ucdashboard.php?stn={station}", verify=False
        )
        soup = BeautifulSoup(r.text, "lxml")
        # print(r.text)
        tables = soup.find_all("ul", class_="container-height-secondary")
        # tables[0] = Unit Details
        # tables[1] = units by status
        # tables[2] = Out of Service
        # tables[3] = Active Events
        # tables[4] = Personnel

        units = []
        for row in tables[0].find_all("tr"):
            if str(row).find("<b>") == -1:
                u = Unit()
                cols = row.find_all("td")
                u.call_sign = cols[0].text.strip()  # [0:5]
                u.unit_type = cols[1].text.strip()
                u.status = cols[2].text.strip()
                if u.status == "OS":
                    for os_row in tables[2].find_all("ul"):
                        os_car = os_row.find("li", id="s5title").find("center").text
                        if os_car == u.call_sign:
                            u.out_of_service_code = (
                                os_row.find("div", id="s5").find("h1").text
                            )
                            u.out_of_service_duration = os_row.find(
                                "span", id="s5_minute"
                            ).text
                u.location = cols[3].text.strip()
                units.append(u)
        for unit in units:
            unit.event_id = None
            unit.event_type = None
            unit.event_sub_type = None
            for ae_row in tables[3].find_all("tr"):
                if str(ae_row).find(unit.call_sign) > 0:
                    ae_cols = ae_row.find_all("td")
                    unit.event_id = ae_cols[1].text.strip()
                    unit.event_type = ae_cols[2].text.strip()
                    unit.event_sub_type = ae_cols[3].text.strip()

        for unit in units:
            for p_row in tables[4].find_all("tr"):
                if str(p_row).find(unit.call_sign) > 0:
                    p_cols = p_row.find_all("td")
                    unit.employee_one = p_cols[1].text.strip()
                    unit.employee_two = p_cols[2].text.strip()
                    unit.unit_phone_number = p_cols[3].text.strip()
        print(f"scraping complete for {station}")
        return units


collector = Collector()
