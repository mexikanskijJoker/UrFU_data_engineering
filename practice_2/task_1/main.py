import json
import numpy as np
from typing import TypedDict


class DataResponse(TypedDict):
    sum: int
    avg: int
    sumMD: int
    avgMD: int
    sumSD: int
    avgSD: int
    matrix_min: int
    matrix_max: int


class Matrix:
    def __init__(self, data):
        self._matrix = data

    def get_matrix_data(self) -> DataResponse:
        min_value, max_value = self._get_matrix_min_and_max()

        return {
            "sum": f"{self._get_matrix_sum()}",
            "avg": f"{self._get_matrix_avg()}",
            "sumMD": f"{self._get_sumMD()}",
            "avgMD": f"{self._get_avgMD()}",
            "sumSD": f"{self._get_sumSD()}",
            "avgSD": f"{self._get_avgSD()}",
            "matrix_min": f"{min_value}",
            "matrix_max": f"{max_value}",
        }

    def _get_matrix_sum(self) -> int:
        return np.sum(self._matrix)

    def _get_matrix_avg(self) -> int:
        return int(self._get_matrix_sum() / np.size(self._matrix))

    def _get_sumMD(self) -> int:
        return sum(np.diag(self._matrix))

    def _get_avgMD(self) -> int:
        return int((self._get_sumMD() / len(np.diag(self._matrix))))

    def _get_sumSD(self) -> int:
        return sum(np.diag(np.fliplr(self._matrix)))

    def _get_avgSD(self) -> int:
        return int(self._get_sumSD() / len(np.diag(np.fliplr(self._matrix))))

    def _get_matrix_min_and_max(self) -> int:
        return np.min(self._matrix), np.max(self._matrix)

    def _get_normalized_matrix(self) -> list[list[float]]:
        return np.divide(self._matrix, self._get_matrix_sum())


def main():
    matrix = Matrix(np.load("matrix_88.npy"))
    with open("res_data.json", "w") as file:
        data = json.dumps(matrix.get_matrix_data(), indent=2)
        file.write(data)
    np.savetxt("normalized_matrix_88.npy", matrix._get_normalized_matrix())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
