#!/bin/python3
from courses import Courses

for course in Courses():
#    print(vars(course))
    if hasattr(course,"_appendices"):
            appendices = course.appendices
            ra = appendices.parse_range_string('all')
            appendices.update_appendices_in_master(ra)
    lectures = course.lectures
    r = lectures.parse_range_string('all')
    lectures.update_lectures_in_master(r)
    lectures.compile_master()
    
