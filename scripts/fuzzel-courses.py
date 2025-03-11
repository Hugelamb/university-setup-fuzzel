#!/usr/bin/python3
from fuzzel import fuzzel

from courses import Courses

courses = Courses()
current = courses.current

try:
    current_index = courses.index(current)
#    args = ['--search', ]
    args = ['--search', current.info['title']]
except ValueError:
    args = []

code, index, selected = fuzzel('Course: ', [c.info['title'] for c in courses], [
    '--lines', len(courses)
] + args)
if index >= 0:
    courses.current = courses[index]
