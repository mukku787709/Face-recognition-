from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True,
                             verbose_name="Identification Number")
    full_name = models.CharField(max_length=100)
    face_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.full_name

    def get_details(self):
        return self.full_name + " " + self.face_id

    def get_present_days(self):
        from attendance.models.WorkingDay import WorkingDay

        present_days = []

        for working_day in WorkingDay.objects.all():
            if self in working_day.get_present_students():
                present_days.append(working_day)

        return present_days

    def get_absent_days(self):
        from attendance.models.WorkingDay import WorkingDay

        present_days = []

        for working_day in WorkingDay.objects.all():
            if self not in working_day.get_present_students():
                present_days.append(working_day)

        return present_days

    def get_freq_seen_by(self):
        from attendance.models.CapturedFrame import CapturedFrame
        caps = CapturedFrame.objects.filter(students=self)
        seen_ins = [cap.camera_name for cap in caps]
        if seen_ins:
            return most_common(seen_ins)
        else:
            return "-"

    def get_last_seen(self):
        from attendance.models.CapturedFrame import CapturedFrame
        cap = CapturedFrame.objects.filter(students=self).last()
        return cap


def most_common(lst):
    return max(set(lst), key=lst.count)
