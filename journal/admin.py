from django.contrib import admin
from journal.models import *
from image_cropping import ImageCroppingMixin


class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):

    change_form_template = "../templates/journal/admin_edit.html"

    def response_change(self, request, obj):
        if "_back" in request.POST:
            return HttpResponseRedirect("/journal/students/{}".format(obj.id))
        return super().response_change(request, obj)


class PersonalInfoModelAdmin(admin.ModelAdmin):

    change_form_template = "../templates/journal/admin_edit.html"

    def response_change(self, request, obj):
        if "_back" in request.POST:
            return HttpResponseRedirect("/journal/students/{}".format(obj.student.id))
        return super().response_change(request, obj)


class AttendanceModelAdmin(admin.ModelAdmin):

    change_form_template = "../templates/journal/admin_edit.html"

    def response_change(self, request, obj):
        if "_back" in request.POST:
            return HttpResponseRedirect("/journal/attendance/{}".format(obj.id))
        return super().response_change(request, obj)


# Register your models here.
admin.site.register(Subject)
admin.site.register(Student, MyModelAdmin)
admin.site.register(Squad)
admin.site.register(Curriculum)
admin.site.register(PersonalInfo, PersonalInfoModelAdmin)
admin.site.register(Penalty)
admin.site.register(Exam)
admin.site.register(Attendance, AttendanceModelAdmin)
admin.site.register(Lesson)
admin.site.register(Event)
admin.site.register(EventParticipant)
