# New file tools
from pathlib import Path
import timeit
import os


def get_all_files_walk(directory='~/'):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def list_test():
    x = get_all_files_walk()
    return list(x)


def get_all_files(directory='~/'):
    return [str(f) for f in Path(directory).rglob('*') if f.is_file()]


# Usage:
num_runs = 1000
run_time = timeit.timeit(get_all_files, number=num_runs)
print(f"The path function took {run_time} seconds to run over {num_runs} runs.")
run_time = timeit.timeit(get_all_files_walk, number=num_runs)
print(f"The walk function took {run_time} seconds to run over {num_runs} runs.")
run_time = timeit.timeit(list_test, number=num_runs)
print(f"The walk list function took {run_time} seconds to run over {num_runs} runs.")


def get_cost_estimate(surface, price_per_gallon):
    """ return cost estimate for painting surface """
