# WebCourse Scrapper
##### Names:
- ⁠⁠⁠Arthur Sapozhnikov ⁠⁠⁠206262412
- Ido Haber 207900473

##### Language
- python version - 2.7

### Project Type
- Big mini-project

### Target
- Help students manage their HW easier.
- We achieve that by scraping the Webcourse to get the assignments dates and names.
- Then show it to them in a nice GUI.

### Code Explaintion
Two main parts:

1. Web scraper:
The Scrapper library we used is BeautifulSoup. We used it to parse and grab HTML pages of the assignments from the webcourse sites.

2. GUI
Which included multipile select windows, that allowed users to choose their courses. The GUI also shows the end result of the scarping in a scrolable window.

### Implemention
We crafted `class CoursePage` that is initated by a course number and grabs all of the relevent information about it.

The main function that does the parsing of the assigments' HTML page is `__get_expected` which uses the BeautifulSoup function `findAll` that separates the HTML page by tags. Then we iterate the result and try to find keyword the indicte assignments like `Expected` or `Due date`.

If that fails (usually becuase the work of Yaniv Hamo isn't producing consistent code and structure), we try finding the relevant information by using REGEX that were designed to fit this case (we don't use that method exclusively as that takes too long).

We also checks for unusual assigment pages that have folders in it (like in the OS course) and handle these too, as they require more work.

If the user selects courses that have no assignments pages (like seminars, projects and advanced topics), we notify him that - the GUI presents the course number (and name) with a short comment ("This course doesn't have an assignments page").

The result are shown in a GUI that lists all the upcoming work you have to do.

### Running

1. Using the `.exe`:

    Run the `.exe` (in the `dist` folder), wait about 30 seconds, enjoy.

2. Running the `.py` files directly:

    Make sure you have the following libraries:
      * Beutifulsoup
      * urllib2
      * easygui
   
   (you can simply run the command `pip install -r requirements.txt` and it will install it automatically)
   
   and run the file `gui_file.py`.
