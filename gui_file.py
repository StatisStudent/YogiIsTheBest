import course_scrapper
import easygui as g
import sys
from course_list import *

msg ="Which courses do you take?"
title = "WebScraper"
choices = get_course_list()
names = map(lambda x: get_name_of_courses(x), choices )
choices =  map(lambda x: u', '.join((x[0], x[1])).encode('utf-8').strip() , zip(choices,names))
# print type(choices[0][0]),int(choices[0][0])
# for x in choices:
#     print x[0],x
# sys.exit(0)
choice = g.multchoicebox(msg, title, choices)
course_output = ""
for x in choice:
    try:
        course_output += course_scrapper.CoursePage(int(x[:6])).get_assignment_data
        course_output += "\n"
    except Exception:
        print int(x[0])


g.textbox("Here are Your upcoming submissions:", "Courses Result",  course_output)

