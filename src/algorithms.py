# algorithms classes in OOP STYLE!!
from functools import wraps
from time import time
from typing import List, Tuple


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
        return sum(result)

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
            if self.weights[i] <= self.capacity:
                self.inter_solutions += 1
                return i, self.values[i]

    def solve(self) -> List[int]:
        greed_result = self.greed_search()
        max_greed_result, max_greed_value = self.max_greed_search()
        greed_value = self.get_total_value(greed_result)
        return greed_result if greed_value > max_greed_value else max_greed_result


class SecondAlg(Algorithm):
    pass


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
    print(TwoApproxAlgorithm(data)())
    print(data.optimal_weights)




