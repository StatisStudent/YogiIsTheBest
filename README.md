# WebCourse Scrapper
##### Names:
- ⁠⁠⁠Arthur Sapozhnikov ⁠⁠⁠206262412
- Ido Haber 207900473

##### Language
- python version - 2.7

### Project Type
- Big mini-project

### Target
- Help students to manage thier HW better.
- We achienve that by scraping Webcourse to get the assignments dates.
- Then show them in a nice GUI.

### Code Explaintion
Two main parts:
1. Web scraper:
The Scrapper lib we used is BeautifulSoup. we used it in order to parse and grab
html pages of the assinments from the webcourse sites.

2. GUI
Which included multipile select windows that allowed users to choose there courses. The GUI also show the end result of the scarping in a scrolable window.

### implemention
We crafted `class CoursePage` that initated by a course name and grabs all the relevent information about it.

The main function that does the parsing of the assigments html page is `__get_expected` which uses the BeautifulSoup function `findAll` that separates html page by tags. Then we iterate the result and try to find keyword the indicte assinment like `Expected` or `Due date`.

If thats fail (mostly becuase the work of Yaniv Hamo isn't preducing consistent code) we tring finding the relevnt information by using REGEX that desiged to fit the case (we don't use that method exclusively as that takes too long)

We also checks for unusual assigment pages that have folders in it (like in OS course) and handle these too, as they require more work.

The result are shown in a GUI that lists all the upcoming work you have to do.

