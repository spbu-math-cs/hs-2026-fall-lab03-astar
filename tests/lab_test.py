import random
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Callable, Dict, Union

from utils.Map import Map
from utils.Node import BaseNode as Node
from utils.utils import make_path, read_task_from_file, convert_string_to_cells, draw


def simple_test(search_function: Callable, task: Union[int, None], *args):
    """
    Function `simple_test` runs `search_function` on one task.
    Use a number from 0 to 24 to choose a specific debug task on a simple map, 
    or use None to select a random task from this pool. 
    The function displays:
     - 'Path found!' and some statistics if a path was found.
     - 'Path not found!' if a path was not discovered.
     - 'Execution error' if an error occurred during the execution of the search_function.
    In the first case, the function also provides a visualization of the task.

    Parameters
    ----------
    search_function : Callable
        Implementation of the search method.
    task : int | None
        A number from 0 to 24 to choose a specific debug task on a simple map,
        or None to select a random task from this pool.
    *args
        Additional arguments passed to the search function.
    """

    def get_map_data():
        map_str = dedent(
            """
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
            . . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . # # . . . . . . . . . . . . . . . 
            . . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
        """
        )
        cells = convert_string_to_cells(map_str)
        return Map(cells)

    task_map = get_map_data()
    starts = [
        (9, 0),
        (13, 0),
        (7, 28),
        (14, 29),
        (4, 1),
        (0, 17),
        (5, 6),
        (5, 20),
        (12, 2),
        (7, 28),
        (11, 9),
        (3, 2),
        (3, 17),
        (13, 20),
        (1, 1),
        (9, 10),
        (14, 6),
        (2, 0),
        (9, 28),
        (8, 6),
        (11, 6),
        (3, 0),
        (8, 9),
        (14, 7),
        (12, 4),
    ]
    goals = [
        (11, 20),
        (2, 19),
        (6, 5),
        (4, 18),
        (9, 20),
        (7, 0),
        (2, 25),
        (12, 4),
        (3, 25),
        (0, 12),
        (4, 23),
        (2, 24),
        (9, 2),
        (1, 6),
        (13, 29),
        (14, 29),
        (2, 28),
        (14, 16),
        (13, 0),
        (1, 27),
        (14, 25),
        (10, 20),
        (12, 28),
        (2, 29),
        (1, 29),
    ]
    lengths = [
        36,
        30,
        30,
        21,
        28,
        24,
        32,
        27,
        42,
        23,
        35,
        37,
        23,
        26,
        40,
        36,
        42,
        28,
        44,
        36,
        38,
        29,
        33,
        42,
        44,
    ]

    if (task is None) or not (0 <= task < 25):
        task = random.randint(0, 24)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    length = lengths[task]

    try:
        (
            found,
            end_node,
            number_of_steps,
            search_tree_size,
            *other_results,
        ) = search_function(task_map, start.i, start.j, goal.i, goal.j, *args)

        if found:
            path, path_length = make_path(end_node)
            correct = int(path_length) == int(length)
            draw(task_map, start, goal, path, *other_results)
            print(
                f"Path found! Length: {path_length}. Search tree size: {search_tree_size}. "
                f"Number of steps: {number_of_steps}. Correct: {correct}"
            )
        else:
            print("Path not found!")
        return

    except Exception as e:
        print(f"Execution error: {e}")
        traceback.print_exc()


def simple_test_not_found(search_function: Callable, task: Union[int, None], *args):
    """
    Tests the `search_function` on a task that is not expected to have a solution.

    Use a number from 0 to 1 to choose a specific debug task
    on a simple map, or use None to select a random task from this pool. 
    The function displays:
     - 'Path found!' and some statistics if a path was found.
     - 'Path not found!' if a path was not discovered (as expected).
     - 'Execution error' if an error occurred during the execution of the search_function.
    The function also provides a visualization of the task instance.

    Parameters
    ----------
    search_function : Callable
        Implementation of the search method.
    task : int | None
        A number from 0 to 1 to choose a specific debug task on a simple map,
        or None to select a random task from this pool.
    *args
        Additional arguments passed to the search function.
    """

    def get_map_data():
        map_str = dedent(
            """
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
            . . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
            . . . # # . . . . . . # # # # . . . . . . # . . . . . . . . 
            . . . # # . . . . . . # . # # . . . . . . # . . . . . . . . 
            . . . # # . . . . . . # . # # . . . . . . # . . . . . . . . 
            . . . # # . . . . . . # . # # . . . . . . # . . . . . . . . 
            . . . # # . . . . . . # # # # . . . . . . # . . . . . . . . 
            . . . . . . . . . . . . . # # . . . . . . # . . . . . . . . 
            . . . . . . . . . . . . . # # . . . . . . # . . . . . . . .
            . . . . . . . . . . . . . # # . . . . . . # . . . . . . . .
        """
        )
        cells = convert_string_to_cells(map_str)
        return Map(cells)

    task_map = get_map_data()
    starts = [(0, 0), (0, 0)]
    goals = [(14, 25), (9, 12)]

    if (task is None) or not (0 <= task < 2):
        task = random.randint(0, 1)

    start = Node(*starts[task])
    goal = Node(*goals[task])

    try:
        (
            found,
            end_node,
            number_of_steps,
            search_tree_size,
            *other_results,
        ) = search_function(task_map, start.i, start.j, goal.i, goal.j, *args)

        if not found:
            draw(task_map, start, goal, None, *other_results)
            print(
                f"Path not found! Search tree size: {search_tree_size}. "
                f"Number of steps: {number_of_steps}. Correct: True"
            )

        else:
            path, path_length = make_path(end_node)
            draw(task_map, start, goal, path, *other_results)
            print(
                f"Path found! Length: {path_length}. Search tree size: {search_tree_size}. "
                f"Number of steps: {number_of_steps}. Correct: False"
            )
        return

    except Exception as e:
        print(f"Execution error: {e}")
        traceback.print_exc()


def massive_test(search_function, data_path, num_of_tasks, *args) -> Dict:
    """
    The `massive_test` function runs the `search_function` on a set of different tasks
    (for example, from the directory `data/`) using *args as optional arguments.
    For every task, it displays a short report:
     - 'Path found!' along with some statistics if a path was found.
     - 'Path not found!' if a path wasn't found.
     - 'Execution error' if an error occurred during the execution of the search_function.

    The function returns a dictionary containing statistics with the following keys:
     - "corr" — correctness of each path length (True/False).
     - "len" — the length of each path (0.0 if a path wasn't found).
     - "st_size" — the size of the resultant search tree for each task.
     - "steps" — the number of algorithm steps for each task.

    Parameters
    ----------
    search_function : Callable
        The implemented search method.
    data_path : str
        Path to the directory containing tasks.
    num_of_tasks : int
        The number of tasks to be used for evaluation.

    Returns
    -------
    stat : Dict
        A dictionary containing statistics.

    """
    stat = {
        "corr": [],
        "len": [],
        "st_size": [],
        "steps": [],
    }

    if num_of_tasks is None or num_of_tasks <= 0:
        print("Incorrect number of tasks. Testing halted!")
        return stat

    task_num = num_of_tasks

    for task_count in range(task_num):
        task_file_name = Path(data_path) / f"{task_count}.map"
        cells, start_i, start_j, goal_i, goal_j, length = read_task_from_file(
            task_file_name
        )
        task_map = Map(cells)
        try:
            (
                found,
                end_node,
                number_of_steps,
                search_tree_size,
                *other_results,
            ) = search_function(task_map, start_i, start_j, goal_i, goal_j, *args)

            if found:
                _, path_length = make_path(end_node)
                correct = int(path_length) == int(length)

                print(
                    f"Task: #{task_count}. Path found! Length: {path_length}. "
                    f"Search tree size: {search_tree_size}. Number of steps: {number_of_steps}. "
                    f"Correct: {correct}"
                )

                stat["len"].append(path_length)
                stat["corr"].append(correct)
            else:
                print(f"Task: #{task_count}. Path not found!")
                stat["len"].append(0.0)
                stat["corr"].append(False)

            stat["st_size"].append(search_tree_size)
            stat["steps"].append(number_of_steps)

        except Exception as e:
            print(f"Execution error: {e}")
            traceback.print_exc()

    return stat
