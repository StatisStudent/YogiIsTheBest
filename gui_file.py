import course_scrapper
import easygui as g
from course_list import *

msg = "Which courses do you take?"
title = "WebScraper"
choices = get_course_list()
# get courses name from number and save to list
names = map(lambda x: get_name_of_courses(x), choices)
# add the name each of the course choices
choices = map(lambda x: u', '.join((x[0], x[1])).encode('utf-8').strip(), zip(choices, names))
# open gui with multiple choice for the user to pick his courses
choice = g.multchoicebox(msg, title, choices)
course_output = ""
for x in choice:
    try:
        # grabs the information about the course
        course_output += course_scrapper.CoursePage(int(x[:6])).get_assignment_data
        course_output += "\n"
    except Exception:
        # handle courses without assignments (like seminars)
        course_output += 'Course \'' + x + '\' doesn\'t contain assgiment page\n\n'

# print the result in gui
g.textbox("Here are Your upcoming submissions:", "Courses Result", course_output)
