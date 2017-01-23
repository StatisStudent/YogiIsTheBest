import urllib2
from bs4 import BeautifulSoup
from datetime import datetime


def prettify_list(lst):
    now = datetime.now()
    return filter(lambda x: string_to_date(x).date() >= now.date(), lst)


def get_ass_name(link):
    tmp = link.h2.getText()
    if tmp != "": return tmp
    return link.h2.contents[0].attrs[u'data-lang-en']


def string_to_date(i):
    if "," in i:
        return datetime.strptime(i, "%d/%m/%Y, %H:%M")
    else:
        return datetime.strptime(i, "%d/%m/%Y")


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

