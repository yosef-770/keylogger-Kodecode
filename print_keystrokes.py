def print_key_log(list_on_words):
    for i, word in enumerate(list_on_words):
        for key, value in word.items():
            if i == len(list_on_words)-1:
                value = value[:-4]
            print("*****", key, "*****")
            print(value)
