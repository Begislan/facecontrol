from lib2to3.fixes.fix_input import context
import datetime
import random

from django.shortcuts import render
from .models import AttendanceRecordInfo, Clock, Lesoons


# Create your views here.
def index(request):
    datas = AttendanceRecordInfo.objects.all()
    # for i in datas:
    #     i.delete()
    # for i in range(500):
    #     AttendanceRecordInfo.objects.create(
    #     person_id= random.randint(10, 30000000),
    #     person_name = 'Person' + str(random.randint(1,100000)),
    #     person_card_no = random.randint(900000, 1000000),
    #     attendance_date_time = str( random.randint(900000, 100000000000) + 1726759547000),
    #     attendance_state = random.randint(0,1),
    #     attendance_method = random.randint(0,15),
    #     device_ip_address = str(random.randint(0,255)) + '.' +str(random.randint(0,255)) + '.'+str(random.randint(0,255)) + '.'+str(random.randint(0,255)),
    #     device_name = "Hooli" + str(random.randint(1,1000)),
    #     snapshots_path = '',
    #     handler = 1,
    #     attendance_utc_time =str( random.randint(900000, 1000000) + 1726759547),
    #     remarks = 2
    #     )
    clocks = Clock.objects.all()
    context = {
        'datas': datas,
        'clocks': clocks,
    }
    return render(request, 'index.html', context)


def poseshennye(request):
    datas = AttendanceRecordInfo.objects.filter(attendance_state=True)
    clocks = Clock.objects.all()

    # Получаем расписание всех уроков
    lessons = Clock.objects.all()

    # Создаем новый список с форматированными датами
    formatted_datas = []
    for data in datas:
        # Преобразуем время из миллисекунд в секунды
        timeIsSecund = data.attendance_date_time / 1000
        dateTime = datetime.datetime.utcfromtimestamp(timeIsSecund)
        formatted_date = dateTime.strftime('%Y-%m-%d %H:%M:%S')

        # Проверяем, попадает ли время посещения в один из уроков
        for lesson in lessons:
            if lesson.start_clock <= dateTime.time() <= lesson.end_clock:
                # Добавляем запись с привязкой к уроку
                formatted_datas.append({
                    'person_id': data.person_id,
                    'person_name': data.person_name,
                    'formatted_date': formatted_date,
                    'device_ip_address': data.device_ip_address,
                    'device_name': data.device_name,
                    'lesson_name': lesson.name_clock,  # Название урока
                })

    context = {
        'datas': formatted_datas,  # Передаем новый список с отформатированными датами
        'clocks': clocks,
    }
    return render(request, 'poseshennye.html', context)


def clock(request, name_clock):
    clocks = Clock.objects.all()
    clock = Clock.objects.filter(name_clock=name_clock).first()
    # Получаем все записи посещений
    attendance_records = AttendanceRecordInfo.objects.all()

    matching_attendances = []
    for record in attendance_records:
        # Преобразуем время посещения из миллисекунд в секунды и затем в формат datetime
        timeIsSecund = record.attendance_date_time / 1000
        attendance_time = datetime.datetime.utcfromtimestamp(timeIsSecund)
        attendance_time_only = attendance_time.time()

        # attendance_time = datetime.utcfromtimestamp(record.attendance_date_time / 1000)  # Используем datetime.datetime
        # attendance_time_only = attendance_time.time()

        # Проверяем, попадает ли время посещения в интервал времени урока
        if clock.start_clock <= attendance_time_only <= clock.end_clock:
            matching_attendances.append({
                'person_id': record.person_id,
                'person_name': record.person_name,
                'attendance_time': attendance_time,
                'device_name': record.device_name,
            })

    # Передаем расписание и отфильтрованные записи посещений в шаблон
    context = {
        'clock': clock,
        'clocks': clocks,
        'attendance_data': matching_attendances,
    }
    return render(request, 'clock.html', context)
