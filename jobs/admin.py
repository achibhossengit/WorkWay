from django.contrib import admin
from jobs.models import Detail, Job, Category
# Register your models here.
admin.site.register(Job)
admin.site.register(Detail)
admin.site.register(Category)