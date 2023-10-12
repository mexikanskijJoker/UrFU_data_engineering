import re


with open("text_1_var_88", "r") as file:
    text_file = file.read()

text_file = re.sub(r"[.!,?]", "", text_file)

splitted_text = text_file.split()

words_count = {word: splitted_text.count(word) for word in splitted_text}

sorted_dict = {
    word: count
    for word, count in sorted(
        words_count.items(), key=lambda item: item[1], reverse=True
    )
}

with open("task_1", "w") as result:
    for key, value in sorted_dict.items():
        result.write(f"{key} : {value}\n")
