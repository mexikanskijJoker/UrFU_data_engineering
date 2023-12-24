import json
import plotly.express as px
import plotly
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_rows", 20, "display.max_columns", 60)


def read_types(file_name):
    dtypes = {}
    with open(file_name, mode="r") as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == "category":
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes


def create_graphs():
    need_dtyps = read_types("dtypes.json")
    df = pd.read_csv(
        "df.csv", usecols=lambda x: x in need_dtyps.keys(), dtype=need_dtyps
    )
    df.info(memory_usage="deep")
    numeric_data = df.select_dtypes(include=["float32", "float64"])

    # # 1. Линейный график
    plt.figure(figsize=(10, 6))
    for activity, group in df.groupby("Region"):
        plt.plot(group["Total Cost"], label=activity)

    plt.title("Зависимость общей стоимости от региона продажи")
    plt.xlabel("Регион")
    plt.ylabel("Общая стоимость")
    plt.legend()
    plt.savefig("my_dataset/plot_1")

    # 2. Столбчатая диаграмма


#     temperature_columns = [
#         "hand temperature (°C)",
#         "chest temperature (°C)",
#         "ankle temperature (°C)",
#     ]
#     df["activityID"] = df["activityID"].astype(str)
#     avg_temperatures = (
#         df.groupby("activityID")[temperature_columns].mean().reset_index()
#     )
#     avg_temperatures = avg_temperatures.melt(
#         id_vars="activityID",
#         var_name="Temperature Type",
#         value_name="Average Temperature",
#     )
#     plt.figure(figsize=(12, 8))
#     sns.barplot(
#         x="activityID",
#         y="Average Temperature",
#         hue="Temperature Type",
#         data=avg_temperatures,
#     )
#     plt.title("Средние температуры для различных видов деятельности")
#     plt.xlabel("Activity ID")
#     plt.ylabel("Average Temperature")
#     plt.legend(title="Temperature Type")
#     plt.xticks(rotation=45, ha="right")
#     plt.savefig("plots/plot_2")

#     # # 3. Кольцевая диаграмма
#     plt.figure(figsize=(8, 8))
#     df["activityID"].value_counts().plot.pie(autopct="%1.1f%%")
#     plt.title("Распределение активностей")
#     plt.savefig("plots/plot_3")

#     # # 4. Тепловая карта
#     plt.figure(figsize=(12, 8))
#     sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
#     plt.title("Карта корреляции")
#     plt.savefig("plots/plot_4")

#     # # 5. Сложный график зависимостей
#     plt.figure(figsize=(12, 8))
#     sns.pairplot(
#         numeric_data[["hand gyroscope X", "hand gyroscope Y", "hand gyroscope Z"]]
#     )
#     plt.suptitle(
#         "Парная диаграмма переменных с оттенком для различных видов деятельности",
#         y=1.02,
#     )
#     plt.savefig("plots/plot_5")


if __name__ == "__main__":
    create_graphs()
