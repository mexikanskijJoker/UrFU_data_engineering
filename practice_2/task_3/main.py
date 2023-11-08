import json
import os
import msgpack


class DataAggregator:
    def __init__(self, file) -> None:
        self._file = file

    def _get_aggregated_data(self) -> dict[str, dict[str, float]]:
        objects = self._get_obj_prices()
        return {
            k: {
                "max_price": max(v),
                "min_price": min(v),
                "avg_price": round(sum(v) / len(v), 2),
            }
            for k, v in objects.items()
        }

    def _get_file_data(self) -> list:
        with open(self._file, "r") as file:
            return json.load(file)

    @staticmethod
    def _get_file_size(file1, file2) -> tuple[int, int]:
        return os.path.getsize(file1), os.path.getsize(file2)

    def _get_obj_prices(self) -> dict[str, list[float]]:
        data = self._get_file_data()
        objects = {obj["name"]: [] for obj in data}
        for k, v in objects.items():
            for obj in data:
                if obj["name"] == k:
                    v.append(obj["price"])
        return objects

    def _save_data(self, json_file, msg_file) -> None:
        data = self._get_aggregated_data()

        with open(json_file, "w") as file:
            json.dump(data, file, indent=2)

        with open(msg_file, "wb") as file:
            msgpack.pack(data, file)


def main():
    aggregator = DataAggregator("products_88.json")
    aggregator._save_data("aggregated_data_88.json", "aggregated_data_88.msgpack")
    # print(
    #     aggregator._get_file_size(
    #         "aggregated_data_88.json", "aggregated_data_88.msgpack"
    #     )
    # ) == 1800, 1325


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
