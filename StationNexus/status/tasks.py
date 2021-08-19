import requests
from background_task import background
from background_task.models import CompletedTask, Task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from time import gmtime, strftime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# needed to ensure the task queue is clear before adding
# and executing a new task with ./manage.py process_tasks
Task.objects.all().delete()
CompletedTask.objects.all().delete()
channel_layer = get_channel_layer()


@background(schedule=5)
def bg_tasks_status(*kwargs):
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), " - background task fired")

    stn_id = 10
    async_to_sync(channel_layer.group_send)(
        f"data_{stn_id}",
        {
            "type": "send_test_data",
        },
    )
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "background task complete")
