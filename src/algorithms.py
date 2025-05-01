# algorithms classes in OOP STYLE!!
from functools import wraps
from time import time
from typing import List

import numpy as np


def measure_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time()
        result = func(self, *args, **kwargs)
        end = time()
        self.execution_time = round(end - start, 6)
        return result
    return wrapper


class KnapsackData:
    def __init__(self, capacity: int, weights: List[int], values: List[int], optimal_weights: List[int]):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.optimal_weights = optimal_weights


class Algorithm:
    def __init__(self, data: KnapsackData):
        self.capacity = data.capacity
        self.weights = data.weights
        self.values = data.values
        self.execution_time = None
        self.inter_solutions = 0

    def get_total_value(self, result: List[int]) -> int:
        return sum(res * value for value, res in zip(self.values, result))

    def get_total_weight(self, result: List[int]) -> int:
        return sum(res * weight for weight, res in zip(self.weights, result))

    def solve(self) -> List[int]:
        pass

    @measure_time
    def __call__(self) -> List[int]:
        return self.solve()

    def get_execution_time(self) -> float:
        return self.execution_time


class TwoApproxAlgorithm(Algorithm):
    def greed_search(self):
        qualities = {i: value / weight for i, weight in enumerate(self.weights) for value in self.values}
        qualities = dict(sorted(qualities.items(), key=lambda quality: quality[1], reverse=True))

        sum_weights = 0
        result = [0] * len(self.weights)
        for item in qualities.keys():
            if sum_weights + self.weights[item] <= self.capacity:
                sum_weights += self.weights[item]
                result[item] = 1
                self.inter_solutions += 1
            if sum_weights == self.capacity:
                break

        return result

    def max_greed_search(self):
        sorted_values = sorted(self.values, reverse=True)

        for i, value in enumerate(sorted_values):
            self.inter_solutions += 1
            if self.weights[i] <= self.capacity:
                return i, self.values[i]

    def solve(self) -> List[int]:
        self.inter_solutions = 0
        greed_result = self.greed_search()
        max_greed_result, max_greed_value = self.max_greed_search()
        greed_value = self.get_total_value(greed_result)
        return greed_result if greed_value > max_greed_value else max_greed_result


class DPWeights(Algorithm):
    def dp_table(self) -> np.ndarray:
        n = len(self.weights)
        W = self.capacity
        table = np.zeros((n + 1, W + 1), dtype=object)

        for i in range(n + 1):
            for w in range(W + 1):
                if i == 0 or w == 0:
                    table[i][w] = (0, 0)
                elif self.weights[i - 1] > w:
                    table[i][w] = (table[i - 1][w][0], w)
                else:
                    w_ind = w - self.weights[i - 1]
                    take = self.values[i-1] + table[i - 1][w_ind][0]
                    no_take = table[i - 1][w][0]
                    if take > no_take:
                        table[i][w] = (take, w_ind)
                    else:
                        table[i][w] = (no_take, w)
                    self.inter_solutions += 1
        return table

    def get_weight_by_table(self, table: np.ndarray) -> List[int]:
        result = [0] * len(self.weights)

        w = self.capacity
        for i in range(len(self.weights), 0, -1):
            _, pre_w = table[i][w]
            if pre_w != w:
                result[i - 1] = 1
            w = pre_w
        return result

    def solve(self) -> List[int]:
        self.inter_solutions = 0
        table = self.dp_table()
        result = self.get_weight_by_table(table)
        return result


class ThirdAlg(Algorithm):
    pass


class FourthAlg(Algorithm):
    pass


class FilesKnapsack:
    def __init__(self, capacity_file: str, weights_file: str, values_file: str, optimal_weights_file: str):
        self.capacity_file = capacity_file
        self.weights_file = weights_file
        self.values_file = values_file
        self.optimal_weights_file = optimal_weights_file


def read_knapsack_data(files: FilesKnapsack) -> KnapsackData:
    with open(files.capacity_file, "r") as f:
        capacity = int(f.readline())
    with open(files.weights_file, "r") as f:
        weights = list(map(int, f.readlines()))
    with open(files.values_file, "r") as f:
        values = list(map(int, f.readlines()))
    with open(files.optimal_weights_file, "r") as f:
        optimal_weights = list(map(int, f.readlines()))

    return KnapsackData(capacity, weights, values, optimal_weights)


if __name__ == "__main__":
    capacity_file = 'benchmarks/p01/p01_c.txt'
    weights_file = 'benchmarks/p01/p01_w.txt'
    values_file = 'benchmarks/p01/p01_p.txt'
    optimal_weights_file = 'benchmarks/p01/p01_s.txt'
    files = FilesKnapsack(capacity_file, weights_file, values_file, optimal_weights_file)

    data = read_knapsack_data(files)
    print(DPWeights(data)())
    print(data.optimal_weights)




