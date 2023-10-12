result = []

with open("text_2_var_88", "r") as file:
    for line in file:
        splitted_line = line.strip("\n").split(",")
        result.append(sum([int(num) for num in splitted_line]))

with open("task_2", "w") as res:
    for number in result:
        res.write(str(number) + "\n")
