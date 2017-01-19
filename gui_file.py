import course_scrapper
import easygui as g
import sys
from course_list import get_course_list

msg ="Which courses do you take?"
title = "WebScraper"
choices = get_course_list()
choice = g.multchoicebox(msg, title, choices)
course_output = ""
for x in choice:
    try:
        course_output += course_scrapper.CoursePage(int(x)).get_assignment_data
        course_output += "\n"
    except Exception:
        print int(x)
        sys.exit(0)

g.textbox("Here are Your upcoming submissions:", "Courses Result",  course_output)

