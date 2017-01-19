import pdb
import urllib2
from bs4 import BeautifulSoup
import unicodedata
import easygui


def get_course_list():
    url = 'https://webcourse.cs.technion.ac.il/'
    soup = BeautifulSoup(urllib2.urlopen((url)), 'html.parser')

    courses = []
    for a in soup.findAll('span')[4].findAll('a'):
        courses.append(unicodedata.normalize('NFKD', a.getText()).encode('ascii', 'ignore'))

    return courses


def get_name_of_courses(course_number):
    url = 'https://webcourse.cs.technion.ac.il/' + course_number
    soup = BeautifulSoup(urllib2.urlopen((url)), 'html.parser')
    name = ""
    for meta in soup.findAll('meta'):
        if u'name' in meta.attrs and meta.attrs[u'name'] == u'Description':
            name = unicodedata.normalize('NFKD', meta.attrs[u'content'].split(u',')[1]).encode('ascii', 'ignore').strip()
            break
    if name == '':
        for span in soup.findAll('span'):
            if u'class' in span.attrs and span.attrs[u'class'][0] == u'titlebarname':
                try:
                    name = span.contents[3].contents[0]
                except:
                    name = span.contents[3].attrs[u'data-lang-en']
                name = name[len('234123'):].strip().replace(u"-","")
                break


    return name
if __name__ == 'main':
    for c in get_course_list():
        print (get_name_of_courses(c))