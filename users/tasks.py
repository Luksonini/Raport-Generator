from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from users.models import ModifiedFile, PDFFile, ExcelFile, DocxZipFile, PdfZipFile, Profile
from django.utils import timezone
from raport_from_list.raport_functions import delete_old_files


class DeleteOldFilesCronJob(CronJobBase):
    # RUN_EVERY_MINS = 24 * 60  # Run the task every hour
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'users.delete_old_files_cron_job'  # Unique code for the task

    def do(self):
        now = timezone.now()

        # Get all user profiles
        profiles = Profile.objects.all()

        for profile in profiles:
            scheduled_deletion_time = profile.next_scheduled_deletion_time

            if scheduled_deletion_time and now >= scheduled_deletion_time:
                delete_old_files(profile)

     
