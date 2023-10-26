result = []

with open("text_3_var_88", "r") as file:
    for line in file:
        line = line.strip("\n").split(",")

        for i in range(len(line)):
            if line[i] == "NA":
                line[i] = str(int((int(line[i - 1]) + int(line[i + 1])) / 2))

        line = list(filter(lambda num: int(num) ** 0.5 >= 50 + 88, line))

        if line != []:
            result.append(line)

with open("task_3", "w") as res_file:
    for res in result:
        res_file.write(",".join(res) + "\n")
