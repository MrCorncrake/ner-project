from tkinter import *
from tkinter import ttk
import random


def window(text: str, found_words: {str: [(int, int)]}):
    root = Tk()
    root.title("Found words in text")
    # mainframe = ttk.Frame(root, padding="3 3 12 12")
    textField = Text(root)

    label = Label(root, background="#a8d3ff")
    label.pack(side="top", fill="x")

    textField.insert(INSERT, text)
    textField.pack(expand=1, fill=BOTH)

    def show_info(text, color):
        label.configure(text=text, fg=color, bg="#a8d3ff")

    for word in found_words:
        hexColor = "#"+''.join([random.choice('AB0123456789') for i in range(6)])
        for coords in word[1]:
            tagID = word[0] + str(coords)
            textField.tag_add(tagID, "1.0+" + str(coords[0]) + "c", "1.0+" + str(coords[1]) + "c")

            # configuring a tag called start
            textField.tag_config(tagID, foreground=hexColor, background="#a8d3ff")

            textField.tag_bind(
                tagID,
                "<Enter>",
                lambda event, curr_word=word[0], curr_color=hexColor: show_info(curr_word, curr_color)
            )
            textField.tag_bind(
                tagID,
                "<Leave>",
                lambda event, curr_word=word[0], curr_color="#000": show_info("", curr_color)
            )

    textField.config(state=DISABLED)

    root.mainloop()
