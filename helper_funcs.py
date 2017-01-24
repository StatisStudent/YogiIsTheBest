import urllib2
from bs4 import BeautifulSoup
from datetime import datetime


def filter_relevant(lst):
    """
    :param lst: A list of due dates
    :return: The list containing only the due dates the are still relevant
    """
    now = datetime.now()
    return filter(lambda x: string_to_date(x).date() >= now.date(), lst)


def get_ass_name(link):
    """
    Extracts the assignment name from a given HTML element
    :param link: HTML element extracted via BeautifulSoup
    :return: The assignment's name
    """
    tmp = link.h2.getText()
    if tmp != "":  # Some webcourses are built bit differently than others so extra caution is needed
        return tmp
    return link.h2.contents[0].attrs[u'data-lang-en']  # When Yaniv Hamo is in-consistent


def string_to_date(i):
    """
    Converts a date-string to a datetime element
    """
    if "," in i:
        return datetime.strptime(i, "%d/%m/%Y, %H:%M")
    else:
        return datetime.strptime(i, "%d/%m/%Y")


def check_folder(url):
    """
    Checks whether the current folder is relevant
    """
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
