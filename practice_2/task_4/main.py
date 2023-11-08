import json as js
import pickle as pkl


class DataUpdater:
    def __init__(self, pkl_file, json_file) -> None:
        self._pkl_file = pkl_file
        self._json_file = json_file

    def _get_objects(self) -> list[dict]:
        with open(self._pkl_file, "rb") as file:
            return pkl.load(file)

    def _get_options(self) -> list[dict]:
        with open(self._json_file, "r") as file:
            return js.load(file)

    def _get_upd_values(self) -> list[dict]:
        data = self._get_objects()
        options = self._get_options()

        for obj in data:
            for option in options:
                if obj["name"] == option["name"]:
                    price = obj["price"]
                    param = option["param"]
                    match option["method"]:
                        case "sum":
                            obj["price"] = round(price + param, 2)
                        case "sub":
                            obj["price"] = round(price - param, 2)
                        case "percent+":
                            obj["price"] = round(price + price * param, 2)
                        case "percent-":
                            obj["price"] = round(price - price * param, 2)
                else:
                    pass

        return data

    def save_data(self, file) -> None:
        with open(file, "wb") as file:
            data = self._get_upd_values()
            pkl.dump(data, file)


def main():
    data_updater = DataUpdater("products_88.pkl", "price_info_88.json")
    data_updater.save_data("updated_data_88.pkl")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
