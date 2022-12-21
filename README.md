# ner-project
Named Entity Recognition project for Intelligent Information Services

## Install spacy library
`python -m spacy download en_core_web_sm`


## Make executable file
```
pyinstaller --noconfirm --onefile --windowed --icon "ikonka.ico" --name "NER" --add-data "./data/constitution/const_library.txt;./data/constitution" --add-data "./data/constitution/const_evaluation.txt;./data/constitution"  "main.py"`
```