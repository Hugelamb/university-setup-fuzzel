#!/usr/bin/python3
import os
from datetime import datetime
from pathlib import Path
import locale 
import re
import subprocess

from config import get_week, DATE_FORMAT, CURRENT_COURSE_ROOT, TERM, EDITOR

locale.setlocale(locale.LC_TIME, "en_AU.utf8")

def number2filename(n):
    print('n in number2filename(n) is ',n)
    return 'apdx_{0:02d}.tex'.format(n)

def filename2number(s):
    return int(str(s).replace('.tex', '').replace('apdx_', ''))

class Appendix():
    def __init__(self, file_path, course):
        with file_path.open() as f:
            for line in f:
                # appendix_match = re.search(r'appendix\{(.*?)\}\{(.*?)\}\{(.*)\}', line)
                appendix_match = re.search(r'chapter\{(.*?)\}\\label\{(.*?)\:(.*?)\}', line)
                if appendix_match:
                    break;
        #date_str = appendix_match.group(2)
        #date = datetime.strptime(date_str, DATE_FORMAT)
        #week = get_week(date)
        print(appendix_match.group(1))
        title = appendix_match.group(1)

        self.file_path = file_path
        #self.date = date
        #self.week = week
        self.number = filename2number(file_path.stem)
        self.title = title
        self.course = course


    def edit(self):
        subprocess.Popen([
            TERM,
            EDITOR,
            f"{str(self.file_path)}"
        ])

    def __str__(self):
        return f'<Appendix {self.course.info["short"]} {self.number} "{self.title}">'

class Appendices(list):
    def __init__(self, course):
        self.course = course
        self.root = course.path
        self.master_file = self.root / 'master.tex'
        list.__init__(self, self.read_files())

    def read_files(self):
        files = self.root.glob('apdx_*.tex')
        return sorted((Appendix(f, self.course) for f in files), key=lambda a: a.number)

    def parse_appendix_spec(self, string):
        if len(self) == 0:
            return 0
        if string.isdigit():
            return int(string)
        #elif string == 'last':
        #    return self[-1].number
        #elif string == 'prev':
        #    return self[-1].number - 1

    def parse_range_string(self, arg):
        all_numbers = [appendix.number for appendix in self]
        if 'appendices' in arg:
            return all_numbers
        return []
        #return [self.parse_appendix_spec]
           
    @staticmethod
    def get_header_footer(filepath):
        part = 0
        header = ''
        footer = ''
        with filepath.open() as f:
            for line in f:
                # order of if-statements is important here!
                if 'end appendices' in line:
                    part = 2

                if part == 0:
                    header += line
                if part == 2:
                    footer += line

                if 'start appendices' in line:
                    part = 1
        return (header, footer)

    def update_appendices_in_master(self, r):
        header, footer = self.get_header_footer(self.master_file)
        body = ''.join(
            ' ' * 4 + r'\input{' + number2filename(number) + '}\n' for number in r)
        self.master_file.write_text(header + body +footer)

    def new_appendix(self):
        if len(self) != 0:
            new_appendix_number = self[-1].number + 1
        else:
            new_appendix_number = 1

        new_appendix_path = self.root / number2filename(new_appendix_number)


        new_appendix_path.touch()
        new_appendix_path.write_text(f'\\chapter{{}}\\label{{chp:}}\n')
        if new_appendix_number == 1:
            self.update_appendices_in_master([1])
        else:
            self.update_appendices_in_master([new_appendix_number - 1, new_appendix_number])
        self.read_files()

        a = Appendix(new_appendix_path, self.course)
        
        return a
    
    def compile_master(self):
        result = subprocess.run(
            ['lualatex', '-f', '-interaction=nonstopmode', str(self.master_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(self.root)
        )
        return result.returncode

if __name__ == "__main__":
    for course in Courses():
        incl_appendices(course)
