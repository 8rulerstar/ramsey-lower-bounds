"""Rebuild the 45-vertex graph and check split-criticality by exhaustive search."""

from itertools import combinations
from pathlib import Path

if not __debug__:
    raise SystemExit("Run without -O so the verification assertions are enabled.")

COLS = range(12)
SHARED_COLUMNS = frozenset(range(4))
SQUARES = {i * i % 17 for i in range(1, 17)}
groups = [tuple(range(start, start + 4)) for start in (0, 4, 8)]


def label_row(group):
    ordered = list(group) + sorted(set(COLS) - set(group))
    return dict(zip(ordered, [0, 0, 3, 6] + sorted(SQUARES)))


labels = [label_row(group) for group in groups]
# Each of the first three rows has 12 vertices. In row 3 one vertex
# belongs to all four shared columns, followed by eight ordinary vertices.
shared_vertex = (3, -1)
vertices = [(r, c) for r in range(3) for c in COLS]
vertices += [shared_vertex] + [(3, c) for c in COLS if c not in SHARED_COLUMNS]
n = len(vertices)
assert n == 45


def column_set(vertex):
    return SHARED_COLUMNS if vertex == shared_vertex else {vertex[1]}


def red(u, v):
    r, c = u
    s, d = v
    if r != s:
        return bool(column_set(u) & column_set(v))
    return r < 3 and (labels[r][c] - labels[r][d]) % 17 in SQUARES


def mask(indices):
    return sum(1 << i for i in indices)


def indices(bits):
    while bits:
        first = bits & -bits
        yield first.bit_length() - 1
        bits ^= first


all_vertices = (1 << n) - 1
red_neighbors = [
    mask(j for j, v in enumerate(vertices) if red(u, v)) for u in vertices
]
matrix = ["".join(str((row >> j) & 1) for j in range(n)) for row in red_neighbors]
stored = Path(__file__).with_name("split45.txt").read_text(encoding="ascii").splitlines()
assert stored == [str(n)] + matrix, "stored adjacency matrix differs from the construction"
blue_neighbors = [
    all_vertices & ~(neighbors | (1 << i)) for i, neighbors in enumerate(red_neighbors)
]

red_fours, blue_fours = [], []
for four in combinations(range(n), 4):
    colors = [bool(red_neighbors[u] & (1 << v)) for u, v in combinations(four, 2)]
    if all(colors):
        red_fours.append(mask(four))
    elif not any(colors):
        blue_fours.append(mask(four))

columns = [mask(i for i, v in enumerate(vertices) if c in column_set(v)) for c in COLS]
assert set(red_fours) == set(columns)
assert len(red_fours) == 12
for r in range(3):
    row = mask(i for i, v in enumerate(vertices) if v[0] == r)
    special = mask(vertices.index((r, c)) for c in groups[r])
    assert [four for four in blue_fours if four & row == four] == [special]


def contains_blue_triangle(chosen):
    # Check all triples without constructing a new graph for each node.
    for a in indices(chosen):
        remaining = chosen & blue_neighbors[a] & ~((1 << (a + 1)) - 1)
        for b in indices(remaining):
            if remaining & blue_neighbors[b]:
                return True
    return False


for r in range(4):
    row_indices = [i for i, v in enumerate(vertices) if v[0] == r]
    assert not any(
        all(red_neighbors[i] & (1 << j) for i, j in combinations(four, 2))
        for four in combinations(row_indices, 4)
    )
    assert all(contains_blue_triangle(mask(nine)) for nine in combinations(row_indices, 9))
    ordinary = mask(i for i in row_indices if not (column_set(vertices[i]) & SHARED_COLUMNS))
    assert contains_blue_triangle(ordinary)


def find_split(chosen=0):
    # The blue-safe side must hit every red K4. If a valid split exists,
    # one of its vertices hits the first unhit red K4. Adding a vertex
    # creates a blue K4 iff its chosen blue neighbors contain a triangle.
    for four in red_fours:
        if chosen & four:
            continue
        for i in indices(four):
            if not contains_blue_triangle(chosen & blue_neighbors[i]):
                answer = find_split(chosen | (1 << i))
                if answer is not None:
                    return answer
        return None
    return chosen


def deletion_split(removed):
    column = min(column_set(vertices[removed]))
    row = next(r for r, group in enumerate(groups) if column in group)
    blue_safe = mask(vertices.index((row, d)) for d in COLS if d != column)
    assert blue_safe & (1 << removed) == 0
    red_safe = all_vertices & ~(blue_safe | (1 << removed))
    assert not any(four & blue_safe == four for four in blue_fours)
    assert not any(four & red_safe == four for four in red_fours)


assert find_split() is None
for removed in range(n):
    deletion_split(removed)
last_row = [i for i, v in enumerate(vertices) if v[0] == 3]
assert len(last_row) == 9
assert all(blue_neighbors[i] & (1 << j) for i, j in combinations(last_row, 2))
print(f"vertices: {n}")
print(f"red K4s: {len(red_fours)} (exactly the columns)")
print("valid splits of the full graph: 0 (exhaustive search)")
print(f"explicit deletion splits verified: {n}/{n}")
print("blue clique in the last row: 9 vertices")
