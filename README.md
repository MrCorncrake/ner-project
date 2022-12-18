# ner-project
Named Entity Recognition project for Intelligent Information Services

## Install spacy library
`python -m spacy download en_core_web_sm`


## Make executable file
`pyinstaller --noconfirm --onefile --windowed --icon "ikonka.ico" --name "NER" --add-data "./data/NZ/NZ_lib.txt;./data/NZ" --add-data "./data/NZ/NZ_text.txt;./data/NZ"  "main.py"`