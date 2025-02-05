from django.contrib import admin

from app.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Posts)
admin.site.register(ResearchPapers)
admin.site.register(FieldsToQuery)