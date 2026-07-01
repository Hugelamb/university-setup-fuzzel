#!/usr/bin/python3
from courses import Courses
from fuzzel import fuzzel

lectures = Courses().current.lectures
appendices = Courses().current.appendices
tutorials = Courses().current.tutorials

commands = ['last', 'prev-last', 'all', 'prev','last_tut', 'all_tut', 'all_with_appendices']
options = ['Current lecture', 'Last two lectures', 'All lectures', 'Previous lectures','Current tutorial','All tutorials','All with appendices']

key, index, selected = fuzzel('Select view', options, [
    '--lines', 7,
])

if index >= 0:
    print(index)
    command = commands[index]
else:
    command = selected

if 'tut' in command:
    tutorials_range = tutorials.parse_range_string(command)
    print(command)
    print(tutorials_range)
    tutorials.update_tutorials_in_master(tutorials_range)
    tutorials.compile_tut_master()
elif command == 'all_with_appendices':
    # add requested appendices to master if not present
    appendices_range = appendices.parse_range_string(command)
    appendices.update_appendices_in_master(appendices_range)
    lectures.compile_master()
else:
    # remove appendices from master if present
    appendices_range = appendices.parse_range_string(command)
    appendices.update_appendices_in_master(appendices_range)
    # add requested lectures to master if not present
    lecture_range = lectures.parse_range_string(command)
    lectures.update_lectures_in_master(lecture_range)
    lectures.compile_master()
