from django.db import models

class AttendanceRecordInfo(models.Model):
    person_id = models.CharField(max_length=30, primary_key=True)
    person_name = models.CharField(max_length=36, null=True, blank=True)
    person_card_no = models.CharField(max_length=20, null=True, blank=True)
    attendance_date_time = models.BigIntegerField()
    attendance_state = models.IntegerField()
    attendance_method = models.IntegerField()
    device_ip_address = models.CharField(max_length=20, null=True, blank=True)
    device_name = models.CharField(max_length=50, null=True, blank=True)
    snapshots_path = models.CharField(max_length=200, default='', blank=True)
    handler = models.CharField(max_length=50, null=True, blank=True)
    attendance_utc_time = models.BigIntegerField(default=0)
    remarks = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'attendancerecordinfo'
        unique_together = (('person_id', 'attendance_date_time'),)
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return self.person_name

class Clock(models.Model):
    name_clock = models.CharField(max_length=100, verbose_name="Урок")
    start_clock = models.TimeField()
    end_clock = models.TimeField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Время урока'

    def __str__(self):
        return f"{self.name_clock}: {self.start_clock} - {self.end_clock}"

class Lesoons(models.Model):
    name_lesson = models.CharField(max_length=255, verbose_name='Название дисциплин')

    def __str__(self):
        return self.name_lesson

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'



