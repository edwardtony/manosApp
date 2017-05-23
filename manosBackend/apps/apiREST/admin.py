from django.contrib import admin

from apps.apiREST.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Worker)
admin.site.register(Address)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(JobRequest)
admin.site.register(Photo)
admin.site.register(JobApplication)