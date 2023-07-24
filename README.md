# FIND NEW BOOKS BY AUTHORS

A python application that lets you check for new books for you favorite writers.

## How it works

1. there is a hardcoded array of authors in webscraper.py > newBooks()
2. the programm visits https://www.bookseriesinorder.com/[author] and scrapes all available books / works
3. if there is a saved file currentbooks.json it will make a copy into files folder
4. it will compare the new results with the old results
5. it returns only the new books / works in a ui window and will create a new_books file in the files folder

## Run it

Make sure python is installed
`python`

Install relevant modules

- BeautifulSoup:
  `pip install bs4`

- Requests:
  `pip install requests`

Run it:
`py controller.py`

Alternatively you can double-click on webscraper.bat
