from django.contrib import admin
from .models import Ssh_key, Repository, Test_info
# Register your models here.

admin.site.register(Ssh_key)
admin.site.register(Repository)
admin.site.register(Test_info)
