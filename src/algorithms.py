# algorithms classes in OOP STYLE!!
from typing import List


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

    def get_total_value(self, result: List[int]) -> int:
        return sum(res * value for value, res in zip(self.values, result))

    def solve(self) -> List[int]:
        pass

    def __call__(self) -> List[int]:
        return self.solve()


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
            if sum_weights == self.capacity:
                break

        return result

    def max_greed_search(self):
        sorted_values = sorted(self.values, reverse=True)

        for i, value in enumerate(sorted_values):
            if self.weights[i] <= self.capacity:
                return i, self.values[i]

    def solve(self) -> tuple[List[int], int]:
        greed_result = self.greed_search()
        max_greed_result, max_greed_value = self.max_greed_search()
        greed_value = self.get_total_value(greed_result)
        return (greed_result, greed_value) if greed_value > max_greed_value else (max_greed_result, max_greed_value)


class SecondAlg(Algorithm):
    pass


class ThirdAlg(Algorithm):
    pass


class FourthAlg(Algorithm):
    pass


def read_knapsack_data(capacity_file: str, weights_file: str, values_file: str,
                       optimal_weights_file: str) -> KnapsackData:
    with open(capacity_file, "r") as f:
        capacity = int(f.readline())
    with open(weights_file, "r") as f:
        weights = list(map(int, f.readlines()))
    with open(values_file, "r") as f:
        values = list(map(int, f.readlines()))
    with open(optimal_weights_file, "r") as f:
        optimal_weights = list(map(int, f.readlines()))

    return KnapsackData(capacity, weights, values, optimal_weights)


if __name__ == "__main__":
    capacity_file = 'benchmarks/p01/p01_c.txt'
    weights_file = 'benchmarks/p01/p01_w.txt'
    values_file = 'benchmarks/p01/p01_p.txt'
    optimal_weights_file = 'benchmarks/p01/p01_s.txt'

    data = read_knapsack_data(capacity_file, weights_file, values_file, optimal_weights_file)
    print(TwoApproxAlgorithm(data)())
    print(data.optimal_weights)




