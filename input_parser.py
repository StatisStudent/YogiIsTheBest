import course_scrapper

# consider a GUI drop down menu
print("Please enter course numbers in a single line, separated with spaces -")
numbers_list = map(int, raw_input().split())
courses_list = []
for i in numbers_list:
    courses_list.append(course_scrapper.CoursePage(i))
for i in courses_list:
    print(i.get_assignment_data)
