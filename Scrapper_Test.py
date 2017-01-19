import course_scrapper

courses = [234123,444444, 236653, 236350, 234122, 44444]
for i in courses:
    try:
        print course_scrapper.CoursePage(i).get_assignment_data
    except:
        print "\nCourse \'" + str(i) + "\' is not a valid CS course number!\n"