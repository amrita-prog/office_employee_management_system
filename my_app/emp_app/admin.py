from django.contrib import admin
from . models import Employee, Role, Department, Attendance

# Register your models here.

admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Attendance)
