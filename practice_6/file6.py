import json
import os
import pandas as pd


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

LINK = "https://excelbianalytics.com/wp/wp-content/uploads/2020/09/5m-Sales-Records.7z"

file_name = "data/5m Sales Records.csv"


column_names = [
    "Region",
    "Country",
    "Item Type",
    "Sales Channel",
    "Order Priority",
    "Order Date",
    "Order ID",
    "Ship Date",
    "Units Sold",
    "Unit Price",
    "Total Revenue",
    "Total Cost",
    "Total Profit",
]


def read_file(file_name):
    return next(pd.read_csv(file_name, chunksize=100_000))


def get_memory_stat_by_column(data):
    mem_usage_stats = data.memory_usage(deep=True)
    total_usage = mem_usage_stats.sum()

    print(f"file in memory size = {total_usage // 1024:10} КБ")
    column_stat = []
    for key in data.dtypes.keys():
        column_stat.append(
            {
                "column_name": key,
                "memory_abs": mem_usage_stats[key] // 1024,
                "memory_per": round(mem_usage_stats[key] / total_usage * 100, 4),
                "dtype": data.dtypes[key],
            }
        )

    column_stat.sort(key=lambda x: x["memory_abs"], reverse=True)

    for column in column_stat:
        print(
            f"{column['column_name']:30} : {column['memory_abs']:10} КБ : {column['memory_per']:10}% : {column['dtype']}"
        )


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024**2

    return "{:03.2f} MB".format(usage_mb)


def opt_float(data):
    dataset_float = data.select_dtypes(include=["float"])
    converted_float = dataset_float.apply(pd.to_numeric, downcast="float")

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ["before", "after"]
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float


def opt_int(data):
    dataset_int = data.select_dtypes(include=["int"])
    converted_int = dataset_int.apply(pd.to_numeric, downcast="unsigned")

    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ["before", "after"]
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int


def opt_obj(data, compression=False):
    converted_obj = pd.DataFrame()
    dataset_obj = data.select_dtypes(include=["object"]).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if compression:
            if num_unique_values / num_total_values < 0.5:
                converted_obj.loc[col] = dataset_obj[col].astype("category")
            else:
                converted_obj[col] = dataset_obj[col]
        else:
            if num_unique_values / num_total_values < 0.5:
                converted_obj.loc[:, col] = dataset_obj[col].astype("category")
            else:
                converted_obj[:, col] = dataset_obj[col]

    return converted_obj


def opt_dataset(data, compression=False):
    optimized_dataset = data.copy()
    converted_int = opt_int(data)
    converted_float = opt_float(data)
    converted_obj = opt_obj(data, compression)

    optimized_dataset[converted_int.columns] = converted_int
    optimized_dataset[converted_float.columns] = converted_float
    optimized_dataset[converted_obj.columns] = converted_obj

    return optimized_dataset


def opt_types(optimized_dataset, file_name):
    need_column = dict()
    opt_dtypes = optimized_dataset.dtypes

    for key in column_names:
        need_column[key] = opt_dtypes[key]
        print(f"{key}: {opt_dtypes[key]}")

    with open("dtypes.json", mode="w") as file:
        dtypes_json = need_column.copy()
        for key in dtypes_json.keys():
            dtypes_json[key] = str(dtypes_json[key])

        json.dump(dtypes_json, file)

    has_header = True
    for chunk in pd.read_csv(
        file_name,
        usecols=lambda x: x in column_names,
        dtype=need_column,
        chunksize=100_000,
    ):
        print(f"chunk memory usage = {mem_usage(chunk)}")
        chunk.to_csv("df.csv", mode="a", header=has_header)
        has_header = False


def main():
    data = read_file(file_name)

    print(f"file size: {os.path.getsize(file_name)}")
    get_memory_stat_by_column(data)
    data.info(memory_usage="deep")

    dataset_obj = data.select_dtypes(include=["object"]).copy()
    converted_obj = opt_obj(data)
    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))

    dataset_int = data.select_dtypes(include=["int"])
    converted_int = opt_int(data)
    print(mem_usage(dataset_int))
    print(mem_usage(converted_int))

    dataset_float = data.select_dtypes(include=["float"])
    converted_float = opt_float(data)
    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    optimized_dataset = opt_dataset(data)
    print(f"default data memory usage = {mem_usage(data)}")
    print(f"optimized dataset memory usage = {mem_usage(optimized_dataset)}")

    get_memory_stat_by_column(optimized_dataset)
    optimized_dataset.info(memory_usage="deep")

    opt_types(optimized_dataset, file_name)


if __name__ == "__main__":
    main()
