import json
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):

    def handle(self, *args, **options):

        PeriodicTask.objects.create(
            interval=IntervalSchedule.objects.get(every=1, period='seconds'),  # we created this above.
            name='Check_status',  # simply describes this periodic task.
            task='study.tasks.check_status_task',  # name of task.
            args=json.dumps(['arg1', 'arg2']),
            kwargs=json.dumps({
                'be_careful': True,
            }),
            expires=datetime.utcnow() + timedelta(seconds=30)
        )