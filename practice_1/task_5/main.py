from bs4 import BeautifulSoup as bs

with open("text_5_var_88", "r") as file:
    file = file.readlines()
    lines = ""
    for line in file:
        lines += line

html = bs(lines, "lxml")

table_element = html.find_all("tr")
elem_values = [value.text.split("\n") for value in table_element]

with open("task_5", "w") as res:
    for elem in elem_values:
        res.write(",".join(elem)[1:] + "\n")
