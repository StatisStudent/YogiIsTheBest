import urllib2
from bs4 import BeautifulSoup
import unicodedata


def get_course_list():
    url = 'https://webcourse.cs.technion.ac.il/'
    soup = BeautifulSoup(urllib2.urlopen((url)), 'html.parser')

    courses = []
    for a in soup.findAll('span')[4].findAll('a'):
        courses.append(unicodedata.normalize('NFKD', a.getText()).encode('ascii', 'ignore'))

    return courses
