# test algorithms on benchmarks
from typing import Type, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from src.algorithms import TwoApproxAlgorithm, read_knapsack_data, Algorithm, FilesKnapsack


class Benchmark:
    def __init__(self):
        self.algorithm_classes: Tuple[Type[Algorithm], ...] = (TwoApproxAlgorithm,)

    def run_all_benchmarks(self):
        results = []
        bench_base = 'benchmarks/p0'
        for bench_id in range(1, 8):
            print('-' * 20)
            print(f'Benchmark #{bench_id}')
            bench_path = bench_base + str(bench_id) + '/p0' + str(bench_id) + '_'
            self.run_one_benchmark(bench_path, results, bench_id)

    def run_one_benchmark(self, bench_path: str, results: list, bench_id: int):
        files = FilesKnapsack(bench_path + 'c.txt', bench_path + 'w.txt', bench_path + 'p.txt', bench_path + 's.txt')
        data = read_knapsack_data(files)
        for algorithm_class in self.algorithm_classes:
            algorithm = algorithm_class(data)
            result = algorithm()

            exec_time = algorithm.execution_time
            inter_solutions =  algorithm.inter_solutions
            expected_weights = data.optimal_weights
            actual_weights = result

            expected_total_weight = algorithm.get_total_weight(expected_weights)
            actual_total_weight = algorithm.get_total_weight(actual_weights)

            expected_value = algorithm.get_total_value(expected_weights)
            actual_value = algorithm.get_total_value(result)
            actual_difference = expected_value - actual_value
            percentage_difference = round((actual_difference / expected_value) * 100, 4)
            print(f'{algorithm_class.__name__}: {percentage_difference}%')

            results.append({'bench_id': bench_id, 'algorithm': algorithm_class.__name__, }) # доделать





if __name__ == '__main__':
    Benchmark().run_all_benchmarks()
