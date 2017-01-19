# import urllib.request
import urllib2

import re
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import helper_funcs
import pdb

class CoursePage:
    def __init__(self, number):
        self.number = str(number)
        self.homepage = 'http://webcourse.cs.technion.ac.il/' + self.number
        soup = BeautifulSoup(urllib2.urlopen(self.homepage), 'html.parser')
        self.assignments = (self.homepage + soup.base.get('href').replace('/' + self.number, '')).replace('news', 'hw')
        self.name = soup.title.string.split(',')[0]
        self.currAssDate = None
        self.lastAss = []
        self.assignments_list = []
        self.__find_assignments()

    def __str__(self):
        return str(self.assignments_list)

    # def __repr__(self):
    #     print str(self.assignments_list)

    @property
    def get_assignment_data(self):
        return "Course "+self.name + "\n\tAssignment " + self.lastAss + "\n\tSubmission Date: " + str(self.currAssDate)

    def __assignment_name_appender(self, link):
        if link.h2 is not None:
            self.lastAss.append(helper_funcs.get_ass_name(link))

    def __get_expected(self, soup):
        lst = []
        list1 = []
        list2 = []
        now = datetime.now()
        for link in soup.findAll('span'):
            x=re.search(r"[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}",link.getText())
            r=re.search(r"(HW|Homework)([0-9]| [0-9])",link.getText())
            if x is not None:
                # print "this is the date",x.group(0) if x is not None else None
                list1.append(x.group(0))
            if r is not None:
                # print "this is the name",r.group(0) if r is not None else None
                list2.append(r.group(0))
            print link.getText()
            #print link.getText()

            if 'Expected' in link.getText():
                for i in link.findAll('tr'):
                    if 'Expected' in i.getText():
                        i = helper_funcs.string_to_date(i.getText())
                        if (now.date() >= i.date()) and ('Due date' in link.getText()):
                            lst.append(helper_funcs.get_due(link))
                            self.__assignment_name_appender(link)
                            break
            elif ('Expected' not in link.getText()) and ('Due date' in link.getText()):
                lst.append(helper_funcs.get_due(link))
                self.__assignment_name_appender(link)

        return zip(list2,list1)
        return lst

    def __folder_get_page(self, soup):
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for j in comments:
            if 'FOLDERS' in j:
                last = j.replace('FOLDERS:', '').replace('-END', '').split(',')
                break
        last.reverse()
        for num in range(0, len(last)):
            last_elem = last[num]
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
            url = self.__folder_get_page(soup)

        soup = BeautifulSoup(urllib2.urlopen((url)), 'html.parser')
        lst = self.__get_expected(soup)
        self.assignments_list = lst
        # lst = helper_funcs.prettify_list(lst)
        # lst.sort(key=lambda d: datetime.strptime(d, "%d/%m/%Y, %H:%M") if ':' in d else datetime.strptime(d, "%d/%m/%Y"))
        # self.currAssDate = lst[0]
        # while len(lst) != len(self.lastAss):
        #     self.lastAss.remove(self.lastAss[0])
        # self.lastAss = self.lastAss[0]