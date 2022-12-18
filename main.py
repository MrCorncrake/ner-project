import nltk

from data.NZ.NZ_evaulation_data import NZ_evaluation_data
from window import window
from ner import EntityLibrary, NamedEntityRecognizer
import os
import sys
from evaluation import accuracy_eval

# nltk.download('punkt')
nltk.download('stopwords')

# Const sample
# file = "const_evaluation.txt"
# lib_file = "library.txt"
# evaluation_data = const_evaluation_data

# NZ sample
file = 'data/NZ/NZ_text.txt'
lib_file = "data/NZ/NZ_lib.txt"
evaluation_data = NZ_evaluation_data

from tkinter import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def calculate():
    print(e1.get())
    try:
        custom_lib_file = e1.get()
        print(custom_lib_file)
        loaded_lib_file = resource_path(custom_lib_file)
        lib = EntityLibrary(loaded_lib_file)
    except:
        loaded_lib_file = resource_path(lib_file)
        lib = EntityLibrary(loaded_lib_file)

    ner = NamedEntityRecognizer(lib)

    try:
        custom_text_file = e2.get()
        print(custom_text_file)
        loaded_text_file = resource_path(custom_text_file)
        lines = open(loaded_text_file, encoding="utf8").read()
    except:
        loaded_text_file = resource_path(file)
        lines = open(loaded_text_file, encoding="utf8").read()

    global master
    master.destroy()

    results = ner.recognize_in(lines, overlapping=False)
    # results = test_spacy_ner()
    # Results
    print(list(results.items()))
    print('')

    accuracy_eval(evaluation_data, results)

    # Visualization
    window(lines, results.items())


if __name__ == '__main__':

    master = Tk()
    Label(master, text="Optional lib file path").grid(row=0)
    Label(master, text="Optional text file path").grid(row=1)

    e1 = Entry(master)
    e2 = Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    Button(master, text='Confirm', command=calculate).grid(row=3, column=1, sticky=W, pady=4)

    master.mainloop()
