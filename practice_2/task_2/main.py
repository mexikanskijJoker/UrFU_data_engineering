import os
import numpy as np


class ValueFilter:
    def __init__(self, data):
        self._matrix = data
        self._x, self._y, self._z = [], [], []

    def get_arrays(self) -> tuple[list[int], list[int], list[int]]:
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                if self._matrix[i][j] > 500 + 88:
                    self._x.append(i)
                    self._y.append(j)
                    self._z.append(self._matrix[i][j])

        return self._x, self._y, self._z

    @staticmethod
    def get_files_size() -> None:
        files = {
            "string_idx.npz": "string_idx_comp.npz",
            "elem_idx.npz": "elem_idx_comp.npz",
            "values.npz": "values_comp.npz",
        }
        for key, value in files.items():
            print(os.path.getsize(key), os.path.getsize(value))

    def save_default_data(self):
        np.savez("string_idx", x=self.get_arrays()[0])
        np.savez("elem_idx", y=self.get_arrays()[1])
        np.savez("values", z=self.get_arrays()[2])

    def save_compressed_data(self):
        np.savez_compressed("string_idx_comp", x=self.get_arrays()[0])
        np.savez_compressed("elem_idx_comp", y=self.get_arrays()[1])
        np.savez_compressed("values_comp", z=self.get_arrays()[2])


def main():
    filter = ValueFilter(np.load("matrix_88_2.npy"))
    filter.save_default_data()
    filter.save_compressed_data()
    filter.get_files_size()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
