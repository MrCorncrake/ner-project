import nltk

from data.NZ.NZ_evaulation_data import NZ_evaluation_data
from data.constitution.const_evaluation_data import const_evaluation_data
from NZ_Eval.text1.short_text1_evaluation_data import short_text1_evaluation_data
from NZ_Eval.text2.short_text2_evaluation_data import short_text2_evaluation_data
from NZ_Eval.text3.short_text3_evaluation_data import short_text3_evaluation_data
from NZ_Eval.text4.short_text4_evaluation_data import short_text4_evaluation_data
from NZ_Eval.text5.short_text5_evaluation_data import short_text5_evaluation_data
from window import window
from ner import EntityLibrary, NamedEntityRecognizer
import os
import sys
from evaluation import accuracy_eval
from tkinter import filedialog
from tkinter import *

# nltk.download('punkt')
nltk.download('stopwords')

# CONSTANTS
DEF_THRESHOLD = 0.25
DEF_FILE = "data/constitution/const_evaluation.txt"
DEF_LIB_FILE = "data/constitution/const_library.txt"
DEF_EVALUATION_DATA = "const_evaluation_data"
EVALUATION_DATAS = {
    "None": None,
    "const_evaluation_data": const_evaluation_data,
    "NZ_evaluation_data": NZ_evaluation_data,
    "short_text1_evaluation_data": short_text1_evaluation_data,
    "short_text2_evaluation_data": short_text2_evaluation_data,
    "short_text3_evaluation_data": short_text3_evaluation_data,
    "short_text4_evaluation_data": short_text4_evaluation_data,
    "short_text5_evaluation_data": short_text5_evaluation_data
}


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def chose_filepath(entry_txt):
    chosen_file = filedialog.askopenfile(mode='r', filetypes=[('all files', '.*'), ('text files', '.txt')])
    if chosen_file:
        filepath = os.path.abspath(chosen_file.name)
        entry_txt.set(filepath)


def calculate():
    if t_spinbox.get() is not None and t_spinbox.get() != "":
        threshold = float(t_spinbox.get())
    else:
        threshold = DEF_THRESHOLD
    print(threshold)
    print(e1.get())
    try:
        custom_lib_file = e1.get()
        print(custom_lib_file)
        loaded_lib_file = resource_path(custom_lib_file)
        lib = EntityLibrary(loaded_lib_file, threshold)
    except:
        loaded_lib_file = resource_path(DEF_LIB_FILE)
        lib = EntityLibrary(loaded_lib_file, threshold)

    ner = NamedEntityRecognizer(lib)

    try:
        custom_text_file = e2.get()
        print(custom_text_file)
        loaded_text_file = resource_path(custom_text_file)
        lines = open(loaded_text_file, encoding="utf8").read()
    except:
        loaded_text_file = resource_path(DEF_FILE)
        lines = open(loaded_text_file, encoding="utf8").read()

    global master
    master.destroy()

    results = ner.recognize_in(lines, overlapping=False)
    # results = test_spacy_ner()
    # Results
    print(list(results.items()))
    print('')

    evaluation_data = EVALUATION_DATAS[eval_data.get()]
    if evaluation_data is not None:
        accuracy_eval(evaluation_data, results)

    # Visualization
    window(lines, results.items())


if __name__ == '__main__':

    master = Tk()
    Label(master, text="Lib file path").grid(row=0)
    Label(master, text="Text file path").grid(row=1)
    Label(master, text="Evaluation data").grid(row=2)
    Label(master, text="Similarity threshold").grid(row=3)

    t1 = StringVar()
    t2 = StringVar()
    e1 = Entry(master, textvariable=t1, width=40)
    e2 = Entry(master, textvariable=t2, width=40)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    eval_data = StringVar()
    eval_data.set(DEF_EVALUATION_DATA)
    d = OptionMenu(master, eval_data, *EVALUATION_DATAS.keys())
    d.grid(row=2, column=1)

    d1 = DoubleVar()
    d1.set(DEF_THRESHOLD)
    t_spinbox = Spinbox(master, textvariable=d1, from_=0, to=1.0, increment=0.01)
    t_spinbox.grid(row=3, column=1)

    Button(master, text='Chose file', command=lambda: chose_filepath(t1)).grid(row=0, column=2, padx=5)
    Button(master, text='Chose file', command=lambda: chose_filepath(t2)).grid(row=1, column=2, padx=5)
    Button(master, text='Confirm', command=calculate).grid(row=4, column=1, pady=6)

    t1.set(resource_path(DEF_LIB_FILE))
    t2.set(resource_path(DEF_FILE))
    master.mainloop()
