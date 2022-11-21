import spacy

text_file = open("const_evaluation.txt", "r").read()

nlp = spacy.load("en_core_web_sm")

doc = nlp(text_file)

word_list = {}

groupings = {
    "united states of america": ["united states", "usa"],
    "representative": ["representatives"],
    "state": ["states"],
    "election": ["elections"],
    "congress": [],
    "senator": ["senators"],
    "president": ["presidents"],
    "house of representatives": [],
    "citizen": ["citizens"],
    "member": ["members"],
    "constitution": ["constitutions"],
    "supreme court": ["court of the united states", "court"],
    "senate": [],
    "section": [],
    "person": ["people"],
    "qualifications": []
}

for ent in doc.ents:
    w_lower = ent.text.lower()
    start_idx = ent.start_char
    end_idx = ent.end_char
    for key, value in groupings.items():
        if w_lower in value:
            if key not in word_list:
                word_list[key] = [(start_idx, end_idx)]
            else:
                word_list[key].append((start_idx, end_idx))
            break
    else:
        if w_lower not in word_list:
            word_list[w_lower] = [(start_idx, end_idx)]
        else:
            word_list[w_lower].append((start_idx, end_idx))

filtered_word_list = {word: word_list[word] for word in groupings.keys() if word in word_list.keys()}

formatted_filtered_word_list = [(key, value) for key, value in filtered_word_list.items()]

print(formatted_filtered_word_list)