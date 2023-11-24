import pickle as pkl


with open("task_2_var_88_subitem.pkl", "rb") as file:
    data = pkl.load(file)


for i in data:
    print(i)
