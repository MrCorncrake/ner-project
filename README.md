# ner-project
Named Entity Recognition project for Intelligent Information Services

## Create virtual environment
Create virtual environment (requires Python 3.8.6 or newer):
```
python -m venv ./venv
```
Activate it (use the right script for bash/cmd/ps):
```
./venv/Scripts/activate.bat
```
Install required libraries:
```
pip install -r requirements.txt
```
## Install spacy library
`python -m spacy download en_core_web_sm`


## Make executable file
```
pyinstaller --noconfirm --onefile --windowed --icon "ikonka.ico" --name "NER" --add-data "./data/constitution/const_library.txt;./data/constitution" --add-data "./data/constitution/const_evaluation.txt;./data/constitution"  "main.py"`
```