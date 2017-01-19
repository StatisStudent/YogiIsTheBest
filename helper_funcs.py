# import urllib.request
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime


def get_rid(word):
    for i in range(0, len(word)):
        try:
            int(word[0])
            return word
        except ValueError:
            word = word[(i+1):len(word)]
    return word


def refactor_string(string):
    for i in range(1, 9):
        month = '/' + str(i) + '/'
        day = str(i) + '/'
        if (month in string) and (string.find(month) > 0):
            string = string.replace(month, '/0' + str(i) + '/')
        if (day in string) and (string.find(day) == 0):
            string = '0' + str(i) + string[1:len(string)]
    return string


def prettify_list(lst):
    now = datetime.now()
    temp_lst = []
    for k in lst:
        if __string_me(k).date() < now.date():
            temp_lst.append(k)
    for k in temp_lst:
        lst.remove(k)
    return lst


def get_ass_name(link):
    return link.h2.getText()


def __string_me(i):
    if ':' in i:
        return datetime.strptime(i, "%d/%m/%Y, %H:%M")
    else:
        return datetime.strptime(i, "%d/%m/%Y")


def string_to_date(i):
    if "," in i:
        i = datetime.strptime(i, "%d/%m/%Y, %H:%M")
    else:
        i = datetime.strptime(i, "%d/%m/%Y")
    return i
#   i = get_rid(i[(len(i.split('/')[0]) - 2):len(i)])
#   i = refactor_string(i)
#   return __string_me(i)1


def check_folder(url):
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url)), 'html.parser')
    now = datetime.now()
    for link in soup.findAll('table'):
        if 'Expected' in link.getText():
            for i in link.findAll('tr'):
                if 'Expected' in i.getText():
                    i = string_to_date(i.getText())
                    if now.date() < i.date():
                        return False
    return True


def get_due(link):
    for i in link.findAll('tr'):
        if 'Due date' in i.getText():
            i = i.getText()
            return refactor_string(i[(len('Due date:  ')):(len(i))])
