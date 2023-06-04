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

        #         # Delete ModifiedFile objects older than the threshold for the current user
        #         modified_files = ModifiedFile.objects.filter(profile=profile, created_at__lt=scheduled_deletion_time)
        #         for modified_file in modified_files:
        #             # modified_file.modyfied_doc_file.delete()  # Delete the file from storage
        #             modified_file.delete()  # Delete the database entry

        #         # Delete PDFFile objects older than the threshold for the current user
        #         pdf_files = PDFFile.objects.filter(profile=profile, created_at__lt=scheduled_deletion_time)
        #         for pdf_file in pdf_files:
        #             # pdf_file.pdf_file.delete()  # Delete the file from storage
        #             pdf_file.delete()

        #         # Delete ExcelFile objects older than the threshold for the current user
        #         excel_files = ExcelFile.objects.filter(profile=profile, created_at__lt=scheduled_deletion_time)
        #         for excel_file in excel_files:
        #             # excel_file.excel_file.delete()  # Delete the file from storage
        #             excel_file.delete()

        #         # Delete DocxZipFile objects older than the threshold for the current user
        #         docx_zip_files = DocxZipFile.objects.filter(profile=profile, created_at__lt=scheduled_deletion_time)
        #         for docx_zip_file in docx_zip_files:
        #             # docx_zip_file.docx_zip_file.delete()  # Delete the file from storage
        #             docx_zip_file.delete()

        #         # Delete PdfZipFile objects older than the threshold for the current user
        #         pdf_zip_files = PdfZipFile.objects.filter(profile=profile, created_at__lt=scheduled_deletion_time)
        #         for pdf_zip_file in pdf_zip_files:
        #             # pdf_zip_file.pdf_zip_file.delete()  # Delete the file from storage
        #             pdf_zip_file.delete()
