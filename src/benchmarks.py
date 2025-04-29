# test algorithms on benchmarks
from typing import Type, Tuple

from src.algorithms import TwoApproxAlgorithm, KnapsackData, read_knapsack_data, Algorithm, FilesKnapsack


class Benchmark:
    def __init__(self):
        self.algorithm_classes: Tuple[Type[Algorithm], ...] = (TwoApproxAlgorithm,)

    def run_all_benchmarks(self):
        bench_base = 'benchmarks/p0'
        for bench_id in range(1, 8):
            print('-' * 20)
            print(f'Benchmark #{bench_id}')
            bench_path = bench_base + str(bench_id) + '/p0' + str(bench_id) + '_'
            self.run_one_benchmark(bench_path)

    def run_one_benchmark(self, bench_path: str):
        files = FilesKnapsack(bench_path + 'c.txt', bench_path + 'w.txt', bench_path + 'p.txt', bench_path + 's.txt')
        data = read_knapsack_data(files)
        for algorithm_class in self.algorithm_classes:
            algorithm = algorithm_class(data)
            result = algorithm()
            print('Execution time:', algorithm.execution_time)
            print('Expected weights', result[0])
            print('Actual weights', data.optimal_weights)
            if result[0] == data.optimal_weights:
                print('Results are same')
            else:
                print('Results are different')
                print('Expected value', algorithm.get_total_value(data.optimal_weights))
                print('Actual value', result[1])


if __name__ == '__main__':
    Benchmark().run_all_benchmarks()
