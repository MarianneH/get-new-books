from view import ui
import subprocess

newBooksResult = newBooks()
ui(newBooksResult)

subprocess.Popen(r"explorer /select," + __file__)
