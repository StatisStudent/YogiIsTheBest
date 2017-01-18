# import urllib.request
import urllib2
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import helper_funcs


class CoursePage:
    def __init__(self, number):
        self.number = str(number)
        self.homepage = 'http://webcourse.cs.technion.ac.il/' + self.number
        soup = BeautifulSoup(urllib2.urlopen(self.homepage), 'html.parser')
        self.assignments = (self.homepage + soup.base.get('href').replace('/' + self.number, '')).replace('news', 'hw')
        self.name = soup.title.string.split(',')[0]
        self.currAssDate = None
        self.lastAss = []
        self.__find_assignments()

    @property
    def get_assignment_data(self):
        return "Course "+self.name + "\n\tAssignment " + self.lastAss + "\n\tSubmission Date: " + str(self.currAssDate)

    def __assignment_name_appender(self, link):
        if link.h2 is not None:
            self.lastAss.append(helper_funcs.get_ass_name(link))

    def __get_expected(self, soup):
        lst = []
        now = datetime.now()
        for link in soup.findAll('table'):
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
        lst = helper_funcs.prettify_list(lst)
        lst.sort(key=lambda d: datetime.strptime(d, "%d/%m/%Y, %H:%M") if ':' in d else datetime.strptime(d, "%d/%m/%Y"))
        self.currAssDate = lst[0]
        while len(lst) != len(self.lastAss):
            self.lastAss.remove(self.lastAss[0])
        self.lastAss = self.lastAss[0]