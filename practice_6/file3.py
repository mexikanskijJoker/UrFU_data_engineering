import os
import pandas as pd


pd.set_option("display.max_rows", 20, "display.max_columns", 60)

FILE_NAME = "data/flights.csv"


def read_file():
    return pd.read_csv(FILE_NAME)


def get_memory_stat_by_column(data):
    mem_usage_stats = data.memory_usage(deep=True)
    total_usage = mem_usage_stats.sum()

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

    return usage_mb


def opt_obj(data):
    converted_obj = pd.DataFrame()
    dataset_obj = data.select_dtypes(include=["object"]).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype("category")
        else:
            converted_obj[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))
    return converted_obj


def opt_int(data):
    dataset_int = data.select_dtypes(include=["int"])
    converted_int = dataset_int.apply(pd.to_numeric, downcast="unsigned")

    print(mem_usage(dataset_int))
    print(mem_usage(converted_int))

    compare_ints = pd.concat([dataset_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ["before", "after"]
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int


def opt_float(data):
    dataset_float = data.select_dtypes(include=["float"])
    converted_float = dataset_float.apply(pd.to_numeric, downcast="float")

    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ["before", "after"]
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float


def opt_dataset(data):
    optimized_dataset = data.copy()
    int = opt_int(data)
    float = opt_float(data)
    obj = opt_obj(data)

    optimized_dataset[int.columns] = int
    optimized_dataset[float.columns] = float
    optimized_dataset[obj.columns] = obj

    print(f"default data memory usage = {mem_usage(data)}")
    print(f"optimized datraset memory usage = {mem_usage(optimized_dataset)}")

    return optimized_dataset


def opt_types(data):
    opt_data = opt_dataset(data)
    opt_dtypes = opt_data.dtypes
    need_column = {}

    column_names = [
        "FLIGHT_NUMBER",
        "ORIGIN_AIRPORT",
        "SCHEDULED_DEPARTURE",
        "DEPARTURE_TIME",
        "DEPARTURE_DELAY",
        "SCHEDULED_TIME",
        "AIR_TIME",
        "DISTANCE",
        "WHEELS_ON",
        "SCHEDULED_ARRIVAL",
    ]

    for key in column_names:
        need_column[key] = opt_dtypes[key]
        print(f"{key}: {opt_dtypes[key]}")

    for chunk in pd.read_csv(
        FILE_NAME,
        usecols=lambda x: x in column_names,
        dtype=need_column,
        parse_dates=["FLIGHT_NUMBER"],
        infer_datetime_format=True,
        chunksize=100_000,
    ):
        print(f"chink memory usage = {mem_usage(chunk)}")
        chunk.to_csv("df3.csv", mode="a")


def get_file_size():
    print(f"file size = {os.path.getsize(FILE_NAME)}")


def main():
    data = read_file()
    get_file_size()
    get_memory_stat_by_column(data)
    opt_obj(data)
    opt_int(data)
    opt_float(data)
    opt_dataset(data)
    opt_types(data)


if __name__ == "__main__":
    main()
