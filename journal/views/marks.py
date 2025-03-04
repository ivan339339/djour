from django.shortcuts import render
from journal.managers.context import with_context
from journal.managers.marks import students_to_keys, tKey, tMark, make_cells
from journal.models import Subject, Mark, Lesson, Student, Attendance, Squad, Exam

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie



@login_required
@ensure_csrf_cookie
def marks_squad(request, squad_code="1702", subject_id=1):
    subj = Subject.objects.filter(id=subject_id).first()
    y_keys = students_to_keys(Student.objects.filter(squad__code=squad_code))
    x_keys = lessons_to_keys(Lesson.objects.filter(attendance__squad__code=squad_code, subject_id=subject_id))
    marks = marks_to_keys(Mark.objects.filter(student__squad__code=squad_code, lesson__subject_id=subject_id))
    header, cells = make_cells(x_keys, y_keys, marks)
    squad = Squad.objects.filter(code=squad_code).first()

    att = Attendance.objects.filter(squad=squad).order_by('-date')

    exams = Exam.objects.filter(subject_id=subject_id, squad=squad)
    print(exams)

    return render(
        request,
        "journal/marks/marks_squad.html",
        with_context({
            "squad_code": squad_code,
            "header": header,
            "cells": cells,
            "marks": marks,
            "subject": subj,
            "x_keys": x_keys,
            "y_keys": y_keys,
            "subject_id": subject_id,
            "attendance_list": att,
            "exam_list": exams,
        })
    )



def marks_to_keys(all_marks: [Mark]) -> [tMark]:
    return [
        tMark(
            id=m.id,
            x_key=m.lesson_id,
            y_key=m.student_id,
            val=m.val,
        ) for m in all_marks
    ]



def lessons_to_keys(lessons: [Lesson]) -> [tKey]:
    return [
        tKey(
            id=l.id,
            display=l.attendance.date.strftime("%d.%m"),
            sort=l.attendance.date,
            val=l.id,
            comment=l.name,
        ) for l in lessons
    ]
