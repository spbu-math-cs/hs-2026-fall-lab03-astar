"""Small assertion checks for the three implementation stages of lab03."""

import io
from contextlib import redirect_stdout

import numpy as np


def _search(search, *args):
    with redirect_stdout(io.StringIO()):
        return search(*args)


def _check_result(result, task_map, start, goal, expected_cost, with_reexpansion=False):
    expected_size = 7 if with_reexpansion else 6
    assert isinstance(result, tuple) and len(result) == expected_size, (
        f"Search must return {expected_size} values."
    )
    found, end, steps, tree_size, opened, expanded = result[:6]
    assert isinstance(found, bool) and found
    assert isinstance(steps, int) and steps >= 0
    assert isinstance(tree_size, int) and tree_size >= 1
    assert end is not None and opened is not None and expanded is not None
    assert (end.i, end.j) == goal
    assert end.g == expected_cost, f"Expected cost {expected_cost}, got {end.g}."

    path = []
    seen = set()
    node = end
    while node is not None:
        point = (node.i, node.j)
        assert point not in seen, "Parent pointers contain a cycle."
        seen.add(point)
        assert task_map.in_bounds(*point) and task_map.traversable(*point)
        path.append(node)
        node = node.parent
    path.reverse()
    assert (path[0].i, path[0].j) == start and path[0].g == 0
    for previous, current in zip(path, path[1:]):
        distance = abs(previous.i - current.i) + abs(previous.j - current.j)
        assert distance == 1, "The path must use only cardinal moves."
        assert current.g == previous.g + 1, "A node has the wrong g-value."
    assert len(path) - 1 == expected_cost
    return result


def _check_unreachable(result, with_reexpansion=False):
    expected_size = 7 if with_reexpansion else 6
    assert isinstance(result, tuple) and len(result) == expected_size
    found, end, steps, tree_size, opened, expanded = result[:6]
    assert found is False and end is None and opened is None
    assert isinstance(steps, int) and steps >= 0
    assert isinstance(tree_size, int) and tree_size >= 1
    assert expanded is not None


def check_astar_basics(Map, Node, SearchTreePQD, manhattan_distance, astar):
    assert manhattan_distance(0, 0, 0, 0) == 0
    assert manhattan_distance(1, 2, 4, 6) == 7
    assert manhattan_distance(4, 6, 1, 2) == 7
    assert Node(0, 0, g=1, h=1) < Node(0, 1, g=3, h=0)

    tree = SearchTreePQD()
    first = Node(0, 0, f=1)
    tree.add_to_open(first)
    tree.add_to_open(Node(0, 0, f=2))
    assert tree.get_best_node_from_open() is first
    tree.add_to_closed(first)
    assert tree.get_best_node_from_open() is None
    assert tree.number_of_open_dublicates == 1

    cases = (
        (np.zeros((1, 1), dtype=np.int8), (0, 0), (0, 0), 0),
        (np.zeros((3, 4), dtype=np.int8), (0, 0), (2, 3), 5),
        (np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]], dtype=np.int8),
         (0, 0), (0, 3), 7),
    )
    for cells, start, goal, cost in cases:
        task_map = Map(cells)
        result = _search(astar, task_map, *start, *goal, manhattan_distance, SearchTreePQD)
        _check_result(result, task_map, start, goal, cost)

    blocked = Map(np.array([[0, 0], [1, 1], [0, 0]], dtype=np.int8))
    _check_unreachable(
        _search(astar, blocked, 0, 0, 2, 1, manhattan_distance, SearchTreePQD)
    )
    print("A* assertion checks passed.")


def check_reexpansion(Map, Node, SearchTreePQDReexp, astar_reexpansion):
    tree = SearchTreePQDReexp()
    old = Node(1, 1, g=5)
    tree.add_to_open(old)
    assert tree.get_best_node_from_open() is old
    tree.add_to_closed(old)
    tree.add_to_open(Node(1, 1, g=6))
    assert tree.open_is_empty(), "A worse route must not reopen CLOSED."
    better = Node(1, 1, g=3)
    tree.add_to_open(better)
    assert not tree.was_expanded(better), "A better route must leave CLOSED."
    assert tree.get_best_node_from_open() is better
    assert better in tree.reexpanded and tree.number_of_reexpansions >= 1

    stale_tree = SearchTreePQDReexp()
    first = Node(0, 0, f=1)
    stale_tree.add_to_open(first)
    stale_tree.add_to_open(Node(0, 0, f=2))
    assert stale_tree.get_best_node_from_open() is first
    stale_tree.add_to_closed(first)
    assert stale_tree.get_best_node_from_open() is None, (
        "Stale OPEN duplicates must not be expanded again."
    )

    # Admissible but inconsistent: this heuristic delays (0, 2), so a longer
    # route reaches another cell first and the shorter route must reopen it.
    def inconsistent(i, j, goal_i, goal_j):
        return abs(goal_i - i) + abs(goal_j - j) if (i, j) == (0, 2) else 0

    task_map = Map(np.zeros((3, 10), dtype=np.int8))
    result = _search(
        astar_reexpansion, task_map, 0, 0, 0, 9, inconsistent, SearchTreePQDReexp
    )
    _check_result(result, task_map, (0, 0), (0, 9), 9, with_reexpansion=True)
    assert result[6] is not None and len(result[6]) > 0, (
        "The inconsistent heuristic should cause at least one re-expansion."
    )
    blocked = Map(np.array([[0, 0], [1, 1], [0, 0]], dtype=np.int8))
    _check_unreachable(
        _search(astar_reexpansion, blocked, 0, 0, 2, 1, inconsistent, SearchTreePQDReexp),
        with_reexpansion=True,
    )
    print("Re-expansion assertion checks passed.")


def check_tie_breakers(Node, lt_g_max, lt_g_min):
    high_g = Node(0, 0, g=4, h=1)
    low_g = Node(0, 1, g=1, h=4)
    lower_f = Node(0, 2, g=1, h=3)
    assert lt_g_max(high_g, low_g) and not lt_g_max(low_g, high_g)
    assert lt_g_min(low_g, high_g) and not lt_g_min(high_g, low_g)
    for compare in (lt_g_max, lt_g_min):
        assert compare(lower_f, high_g) and not compare(high_g, lower_f)
    print("Tie-breaker assertion checks passed.")
