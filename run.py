import math
import os
from contextlib import contextmanager
from time import time
from functools import reduce
from operator import concat
from concurrent.futures import ThreadPoolExecutor, as_completed
from core import solve_puzzle


@contextmanager
def timer():
    t = time()
    yield
    total = time() - t
    print(f'Time taken: {total:.4f}s')


def batch_solve(puzzles):
    return [solve_puzzle(puzzle) for puzzle in puzzles]


def thread_batch_solve(puzzles, workers=4):
    """
    solving using threads
    :param puzzles:
    :param workers:
    :return solved puzzle:
    """
    # assert len(puzzles) >= workers
    dimension = math.ceil(len(puzzles) / workers)
    chunks = (puzzles[n:n+dimension] for n in range(0, len(puzzles), dimension))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = (executor.submit(batch_solve, chunk) for chunk in chunks)
        results = (future.result() for future in as_completed(futures))
        return reduce(concat, results)


puzzles_file = os.path.join(os.getcwd(), 'puzzles.txt')
solutions_file = os.path.join(os.getcwd(), 'solutions.txt')

with open(puzzles_file) as file:
    puzzles_to_solve = [puzzle.strip() for puzzle in file]

with timer():
    solved = batch_solve(puzzles_to_solve)
    with open(solutions_file, 'w') as solutions:
        for grid in solved:
            solutions.write(7 * '/')
            solutions.write(f' Sudoku {solved.index(grid) + 1} ')
            solutions.write(9 * '/')
            solutions.write('\n\n')
            for key, value in grid.items():
                if key not in ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9']:
                    print(value, end='  ', file=solutions)
                else:
                    print(value, '\n', file=solutions)
        solutions.write(26 * '/')
        solutions.write('\n\n')

with timer():
    thread_solved = thread_batch_solve(puzzles_to_solve)
    print(thread_solved)