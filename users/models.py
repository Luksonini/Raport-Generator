
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from datetime import datetime, timedelta


def get_upload_path(instance, filename):
    return f"{instance.user.username}/doc_documents/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc_file = models.FileField(upload_to=get_upload_path, blank=True)
    next_scheduled_deletion_time = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)  # deletes the model instance from the database

    def __str__(self):
        return self.user.username


def get_modified_upload_path(instance, filename):
    return f"{instance.profile.user.username}/modified_doc_documents/{filename}"

class ModifiedFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    modyfied_doc_file = models.FileField(upload_to=get_modified_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.modyfied_doc_file:
            storage, path = self.modyfied_doc_file.storage, self.modyfied_doc_file.path
            super().delete(*args, **kwargs)  # deletes the model instance from the database
        storage.delete(path)  # deletes the file from the filesystem

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.profile.next_scheduled_deletion_time = self.created_at + timedelta(days=1)
        self.profile.save()

    def __str__(self):
        return self.modyfied_doc_file.name


def get_pdf_upload_path(instance, filename):
    return f"{instance.profile.user.username}/modified_doc_documents/{filename}"


class PDFFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, path = self.pdf_file.storage, self.pdf_file.path
        super().delete(*args, **kwargs)  # deletes the model instance from the database
        storage.delete(path)  # deletes the file from the filesystem

    def __str__(self):
        return self.pdf_file.name


def get_excel_upload_path(instance, filename):
    return f"{instance.profile.user.username}/excel_documents/{filename}"


class ExcelFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    excel_file = models.FileField(upload_to=get_excel_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, path = self.excel_file.storage, self.excel_file.path
        super().delete(*args, **kwargs)  # deletes the model instance from the database
        storage.delete(path)  # deletes the file from the filesystem

    def __str__(self):
        return self.excel_file.name


def get_docx_zip_upload_path(instance, filename):
    return f"{instance.profile.user.username}/doc_zip_documents/{filename}"

class DocxZipFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    docx_zip_file = models.FileField(upload_to=get_docx_zip_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, path = self.docx_zip_file.storage, self.docx_zip_file.path
        super().delete(*args, **kwargs)  # deletes the model instance from the database
        storage.delete(path)  # deletes the file from the filesystem

    def __str__(self):
        return self.docx_zip_file.name


def get_pdf_zip_path(instance, filename):
    return f"{instance.profile.user.username}/pdf_zip/{filename}"

class PdfZipFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pdf_zip_file = models.FileField(upload_to=get_pdf_zip_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        storage, path = self.pdf_zip_file.storage, self.pdf_zip_file.path
        super().delete(*args, **kwargs)  # deletes the model instance from the database
        storage.delete(path)  # deletes the file from the filesystem

    def __str__(self):
        return self.pdf_zip_file.name

@receiver(post_delete, sender=Profile)
def delete_profile_doc_file(sender, instance, **kwargs):
    if instance.doc_file:
        instance.doc_file.delete(False)

@receiver(post_delete, sender=ModifiedFile)
def delete_mod_file(sender, instance, **kwargs):
    instance.modyfied_doc_file.delete(False)

@receiver(post_delete, sender=PDFFile)
def delete_pdf_file(sender, instance, **kwargs):
    instance.pdf_file.delete(False)

@receiver(post_delete, sender=ExcelFile)
def delete_excel_file(sender, instance, **kwargs):
    instance.excel_file.delete(False)

@receiver(post_delete, sender=DocxZipFile)
def delete_docx_zip_file(sender, instance, **kwargs):
    instance.docx_zip_file.delete(False)

@receiver(post_delete, sender=PdfZipFile)
def delete_pdf_zip_file(sender, instance, **kwargs):
    instance.pdf_zip_file.delete(False)