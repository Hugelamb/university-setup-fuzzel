#!/usr/bin/python3
from courses import Courses
lectures = Courses().current.lectures

new_lecture = lectures.new_lecture()
new_lecture.edit()

