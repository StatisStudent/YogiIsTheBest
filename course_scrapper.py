import urllib2
import re
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import helper_funcs
import unicodedata


class CoursePage:
    """
    This is the main class that does the parsing. For each course we create a new instance of this class and it will
    take care of the webcourse's parsing - search for and present the date of the latest assignment available.
    """

    def __init__(self, number):
        # Save basic info
        self.number = str(number)
        self.homepage = 'http://webcourse.cs.technion.ac.il/' + self.number

        # Saves the assignments section url
        soup = BeautifulSoup(urllib2.urlopen(self.homepage), 'html.parser')
        self.assignments = (self.homepage + soup.base.get('href').replace('/' + self.number, '')).replace('news', 'hw')
        self.name = soup.title.string.split(',')[0]

        self.currAssDate = None  # Current assignment date
        self.lastAss = []  # Is used to store all of the relevant assignments names
        self.assignments_list = []  # Is used to store all of the relevant assignments dates

        self.__find_assignments() # Starting the parsing job
        # side note - some of these fields are redundant and are here for readability

    def __str__(self):
        return str(self.assignments_list)

    @property
    def get_assignment_data(self):
        """
        We use this method in order to present our results.
        :return: A pretty string presenting the latest assignment's  name and date
        """
        name = "Course " + self.unicode_to_str(self.name)
        ass = "There are currently no active assignments" if not self.lastAss else "Assignment " + self.lastAss
        date = "" if not self.lastAss else "\n\tSubmission Date: " + self.currAssDate
        return name + "\n\t" + ass + date + '\n'

    def __assignment_name_appender(self, link):
        if link.h2 is not None:
            self.lastAss.append(self.unicode_to_str(helper_funcs.get_ass_name(link)))

    def __get_expected(self, soup):
        """
        :return: A list containing the dates of all of the assignments (if its a folder then all of the assignments in
          a given folder).
          If the assignment hasn't been released yet it ignores it.
        We also update lastAss variable to contain a list of the names of all the assignments (side note: if the regex
         were used there is no need to update it)
        """
        lst = []
        now = datetime.now()

        '''
        Our main was to use BeautifulSoup to parse all of what we needed (otherwise what's the point) but since very few
        webcourses (like 3 or 4) are built very poorly it requires extra parsing and it simply takes too long to run it
        (it throws an exception in theses cases) so we decided to use regex to take care of these bastards for runtime
        sake. Tank you for being in-consistent Yaniv Hamo.
        '''
        try:
            for link in soup.findAll('table'):
                expected = ''
                due = ''
                for t in link.findAll('tr'):
                    for s in t.findAll('span'):
                        if u'data-lang-en' in s.attrs and u'Expected' in s.attrs[u'data-lang-en']:
                            expected = helper_funcs.string_to_date(self.unicode_to_str(t.contents[1].getText()))

                        if u'data-lang-en' in s.attrs and u'Due date' in s.attrs[u'data-lang-en']:
                            due = helper_funcs.string_to_date(self.unicode_to_str(t.contents[1].getText()))

                if due != '' or expected != '':
                    if expected != '' and now.date() >= expected.date() and due != '':
                        lst.append(str(due.day) + '/' + str(due.month) + '/' + str(due.year))
                        self.__assignment_name_appender(link)
                    elif expected == '' and due != '':
                        lst.append(str(due.day) + '/' + str(due.month) + '/' + str(due.year))
                        self.__assignment_name_appender(link)

            return lst
        except Exception:
            list1 = []
            list2 = []
            for link in soup.findAll('span'):
                x = re.search(r"[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}", link.getText())
                r = re.search(r"(HW|Homework)([0-9]| [0-9])", link.getText())
                if x is not None:
                    list1.append(x.group(0))
                if r is not None:
                    list2.append(r.group(0))
            return zip(list2, list1)

    @staticmethod
    def unicode_to_str(uni_str):
        """
        Converts a UTF-8 string to a regular string
        """
        return unicodedata.normalize('NFKD', uni_str).encode('ascii', 'ignore')

    def __folder_get_page(self, soup):
        """
        Some courses show their assignments in folders (i.e a separate page for each assignment rather than a single
        page for all of them). This method finds the relevant folder (e.g the staff decided to publish all of the
        assignments' folders [each folder has an 'expected release date' for when to HW is published], we find which
        folder is relevant and return it [i.e expected release date > current date and due date <= current date])
        """
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        # the folders' names are saved as an HTML comment on the webcourse
        for j in comments:
            if 'FOLDERS' in j:
                # lst is a list containing the folders' names. Hw1, Hw2, ....
                lst = j.replace('FOLDERS:', '').replace('-END', '').split(',')
                break
        lst.reverse()  # Hw4, Hw3, ...
        '''
        We iterate from the latest folder, for each folder we extract its link. For every folder we then
        check: its expected release date <= current date. If its true - that's the current task (since we iterated
        from oldest to newest we are bound to find the right one).
        '''
        for num in range(0, len(lst)):
            last_elem = lst[num]
            for link in soup.findAll('a'):
                if (last_elem in link.get('href')) or (last_elem in link.getText()):
                    temp = link
                    break
            url = self.assignments.replace('hw.html', temp.get('href'))
            if helper_funcs.check_folder(url):
                return url

    def __find_assignments(self):
        soup = BeautifulSoup(urllib2.urlopen(self.assignments), 'html.parser')
        url = self.assignments

        # meaning the assignments are in folders
        if 'FOLDERS:-END' not in soup.findAll(text=lambda text: isinstance(text, Comment)):
            # here we replace the assignment page with the relevant folder
            url = self.__folder_get_page(soup)

        soup = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
        lst = self.__get_expected(soup)
        self.assignments_list = lst
        lst = helper_funcs.filter_relevant(lst)

        if not lst:  # it means that there are no relevant assignments left/ever existed
            self.lastAss = []
            return

        self.currAssDate = lst[0]

        # Now we want to filter the irrelevant assignments names
        while len(lst) != len(self.lastAss):
            # remove the hw name
            self.lastAss.remove(self.lastAss[0])
        self.lastAss = self.lastAss[0]  # Save the relevant assignment name
