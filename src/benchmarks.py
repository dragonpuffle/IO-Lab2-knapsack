# test algorithms on benchmarks
from typing import Type, Tuple

import pandas as pd

from src.algorithms import TwoApproxAlgorithm, read_knapsack_data, Algorithm, FilesKnapsack, DPWeights


class Benchmark:
    def __init__(self, algorithm_classes: Tuple[Type[Algorithm], ...]):
        self.algorithm_classes = algorithm_classes

    def run_all_benchmarks(self):
        results = []
        results_diff = []
        bench_base = 'benchmarks/p0'
        for bench_id in range(1, 8):
            print('-' * 20)
            print(f'Benchmark #{bench_id}')
            bench_path = bench_base + str(bench_id) + '/p0' + str(bench_id) + '_'
            self.run_one_benchmark(bench_path, results, results_diff, bench_id)

        data = pd.DataFrame(results).sort_values(by=['bench id', 'algorithm'], axis=0)
        print(data)
        data.to_csv('report.csv', index=False, encoding='utf-8')

        data_diff = pd.DataFrame(results_diff).sort_values(by=['bench id', 'algorithm'], axis=0)
        data_diff.to_csv('report_diff.csv', index=False, encoding='utf-8')

    def run_one_benchmark(self, bench_path: str, results: list, results_diff: list, bench_id: int):
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

            results.append({'bench id': bench_id, 'algorithm': algorithm_class.__name__, 'time': exec_time,
                            'number of inter solutions': inter_solutions, 'alg weights': actual_weights,
                            'alg total weight': actual_total_weight, 'alg profit': actual_value})

            results_diff.append({'bench id': bench_id, 'algorithm': algorithm_class.__name__, 'time': exec_time,
                            'number of inter solutions': inter_solutions, 'alg weights': actual_weights,
                            'expected weights': expected_weights, 'capacity': data.capacity,
                            'alg total weight': actual_total_weight,
                            'expected total weight': expected_total_weight, 'alg profit': actual_value,
                            'expected profit': expected_value, 'profit difference': actual_difference,
                            'percentage profit difference': percentage_difference})



if __name__ == '__main__':
    algs = (TwoApproxAlgorithm, DPWeights)
    Benchmark(algs).run_all_benchmarks()
