from django.contrib import admin
from. models import Profile, PDFFile, ModifiedFile, ExcelFile, DocxZipFile, PdfZipFile

# Register your models here.
admin.site.register(Profile)
admin.site.register(ModifiedFile)
admin.site.register(PDFFile)
admin.site.register(ExcelFile)
admin.site.register(DocxZipFile)
admin.site.register(PdfZipFile)





