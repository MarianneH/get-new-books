import re
import json
import shutil
import datetime
import requests
import os.path
from bs4 import BeautifulSoup


def _copyFile(filename):
    copyFolderName = "files/"
    original = filename
    target = (
        copyFolderName
        + "old_books_"
        + datetime.date.today().strftime("%d-%m-%Y")
        + ".json"
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
            if not author in oldBibliography:
                authorString = author.split("-")
                authorString = [word.capitalize() for word in authorString]
                authorString = " ".join(authorString)

                new_books.append(authorString + " - " + book)

            elif not book in oldBibliography[author]:
                authorString = author.split("-")
                authorString = [word.capitalize() for word in authorString]
                authorString = " ".join(authorString)

                new_books.append(authorString + " - " + book)
    return new_books


def _getNewDataFromWebsite(authors):
    bibliography = json.loads("""{}""")
    url = "https://www.bookseriesinorder.com/"

    for author in authors:
        books = []

        page = requests.get(url + author)
        soup = BeautifulSoup(page.content, "html.parser")
        elements = soup.find_all("td", class_="booktitle")
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
        "sally-rooney",
    ]
    filename = "currentbooks.json"

    oldFileExists = os.path.isfile(filename)

    if oldFileExists:
        _copyFile(filename)
        oldBibliography = _getOldData(filename)

    bibliography = _getNewDataFromWebsite(authors)

    _generateFile(bibliography, filename)

    if not oldFileExists:
        print("no old json available")
        return [False]
    elif bibliography == oldBibliography:
        print("looks like there is nothing new")
        return [False]
    else:
        print("we have a new book")

        newBooks = _getNewBooks(authors, bibliography, oldBibliography)
        newBooksFolder = "newbooks/"

        newBooksFilename = (
            newBooksFolder
            + "new_books_"
            + datetime.date.today().strftime("%d-%m-%Y")
            + ".json"
        )

        _generateFile(newBooks, newBooksFilename)

        return [True, newBooks]
