#!/usr/bin/python3
from courses import Courses
appendices = Courses().current.appendices

new_appendix = appendices.new_appendix()
new_appendix.edit()

