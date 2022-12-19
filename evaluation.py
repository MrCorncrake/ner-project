from functools import reduce


def accuracy_eval(evaluation_data, results):
    total_are = 0
    total_found = 0

    for word in evaluation_data:
        total_are += len(word[1])
        print(word[0] + ": " + str(len(word[1])))
        if word[0] in results:
            print(word[0] + ": " + str(len(results[word[0]])))
            total_found += len(results[word[0]])
        else:
            print(word[0] + ": 0")

    all_letters = 0
    matching_letters = 0

    for word in evaluation_data:
        if word[0] in results:
            for word_position in word[1]:
                found = 0
                for found_word_position in results[word[0]]:
                    if not (
                            found_word_position[0] < word_position[0] and found_word_position[1] < word_position[1]
                            or found_word_position[0] > word_position[0] and found_word_position[1] > word_position[1]
                    ):
                        found += 1
                        all_letters += word_position[1] - word_position[0]
                        matching_letters += word_position[1] - word_position[0] \
                                            - max(0, found_word_position[0] - word_position[0]) \
                                            - max(0, word_position[1] - found_word_position[1])
                if found == 0:
                    all_letters += word_position[1] - word_position[0]
        else:
            print(all_letters)
            all_letters += reduce(lambda total, position: total + position[1] - position[0], word[1], 0)

    print("word accuracy: " + str(total_found / total_are))
    print("letter accuracy: " + str(matching_letters / all_letters))