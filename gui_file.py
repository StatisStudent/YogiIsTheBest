import course_scrapper
import easygui as g
from course_list import *

msg = "Which courses do you take?"
title = "WebScraper"
choices = get_course_list()
names = map(lambda x: get_name_of_courses(x), choices)
choices = map(lambda x: u', '.join((x[0], x[1])).encode('utf-8').strip(), zip(choices, names))

choice = g.multchoicebox(msg, title, choices)
course_output = ""
for x in choice:
    try:
        course_output += course_scrapper.CoursePage(int(x[:6])).get_assignment_data
        course_output += "\n"
    except Exception:
        course_output += 'Course \'' + x + '\' doesn\'t contain assgiment page\n\n'

g.textbox("Here are Your upcoming submissions:", "Courses Result", course_output)
