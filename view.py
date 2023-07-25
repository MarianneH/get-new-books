from tkinter import *


def ui(newBooks):
    root = Tk()

    headline = Label(root, text="Any new books?", font=("Helvetica", 14))
    headline.pack(padx=10, pady=10)

    if newBooks[0]:
        yesBooksLabel = Label(root, text="We have new books!", foreground="green")
        yesBooksLabel.pack()

        root.geometry("450x" + str(22 * len(newBooks[1]) + 90))

        books = newBooks[1]
        for book in books:
            bookLabel = Label(root, text=book)
            bookLabel.pack()
    else:
        noBooksLabel = Label(root, text="No new books!", foreground="red")
        noBooksLabel.pack()

        root.geometry("450x300")

    root.mainloop()
