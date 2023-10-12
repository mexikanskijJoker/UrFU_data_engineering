AGE_CONDITION = 25 + (88 % 10)
salary_list, res, lines = [], [], []

with open("text_4_var_88", "r") as file:
    for line in file:
        line = line.split(",")
        line.pop(5)
        lines.append(line)

        salary_list.append(line[4][:-1])


AVG_SALARY = sum([int(salary) for salary in salary_list]) / len(salary_list)

for line in lines:
    if int(line[3]) > AGE_CONDITION and int(line[4][:-1]) >= AVG_SALARY:
        res.append(line)
    else:
        line = ""

res = sorted(res, key=lambda line: line[0])

with open("task_4", "w") as result:
    for line in res:
        result.write(",".join(line) + "\n")
