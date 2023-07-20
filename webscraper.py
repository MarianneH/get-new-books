import re
from selenium import webdriver
import json
import shutil
import datetime

copyFolderName = "files/"


def _copyFile(filename):
    original = filename
    target = (
        copyFolderName + datetime.date.today().strftime("%d-%m-%Y") + "_old_books.json"
    )

    shutil.copyfile(original, target)


def _getOldData(filename):
    with open(filename, "r") as oldFile:
        oldData = json.load(oldFile)

        return oldData


def _getNewBooks(authors, bibliography, oldBibliography):
    new_books = []
    for author in authors:
        books = bibliography[author]

        for book in books:
            if not book in oldBibliography[author]:
                authorString = author.split("-")
                authorString = [word.capitalize() for word in authorString]
                authorString = " ".join(authorString)

                new_books.append(authorString + " - " + book)
    return new_books


def _getNewDataFromSite(authors):
    bibliography = json.loads("""{}""")
    url2 = "https://www.bookseriesinorder.com/"
    xpath2 = '//*[@class="booktitle"]'

    driver = webdriver.Chrome()

    for author in authors:
        books = []

        driver.get(url2 + author)

        elements = driver.find_elements("xpath", xpath2)

        for element in elements:
            # Extract the text from the element
            fullTitle = element.text

            # Remove the text in the span element using regular expression
            cleanedTitle = re.sub(r"\s*\(By:[^)]*\)\s*", "", fullTitle)

            books.append(cleanedTitle)

        bibliography[author] = books

    return bibliography


def _generateFile(data, filename):
    newJson = json.dumps(data)

    with open(filename, "w") as outfile:
        outfile.write(newJson)


def newBooks():
    authors = [
        "kristin-hannah",
        "adrian-tchaikovsky",
        "elizabeth-strout",
        "james-s-a-corey",
    ]
    filename = "currentbooks.json"

    _copyFile(filename)

    bibliography = _getNewDataFromSite(authors)
    oldBibliography = _getOldData(filename)

    _generateFile(bibliography, filename)

    if bibliography == oldBibliography:
        return [False]
    else:
        print("we have a new book")

        newBooks = _getNewBooks(authors, bibliography, oldBibliography)
        newBooksFilename = (
            copyFolderName
            + datetime.date.today().strftime("%d-%m-%Y")
            + "_new_books.json"
        )

        _generateFile(newBooks, newBooksFilename)

        return [True, newBooks]
