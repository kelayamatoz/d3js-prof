import re
from dataclasses import dataclass
from collections import OrderedDict

N_INDENT = 2

@dataclass
class Node:
    name: str
    cycles_per_iter: int
    n_iters: int
    total_cycles: int
    note: str

def extract(s: str) -> Node:
    s = s.strip()
    name, info = s.split(' - ')
    cycles_per_iter, cycle_info = info.split(' (')
    cycle_info, notes = cycle_info.split(') ')
    total_cycles, n_iters = cycle_info.split(' / ')
    return Node(name, int(cycles_per_iter), int(n_iters), int(total_cycles), notes)

def n_leading_spaces(s: str) -> int:
    return len(s) - len(s.lstrip(' '))

with open('./files/instrumentation.txt') as f:
    perf = f.readlines()[1:]

max_leading_spaces = max([n_leading_spaces(p) for p in perf])

path = list()
last_indent = 0
with open('./files/perf.csv', 'w+') as f:
    for i, p in enumerate(perf):
        n = extract(p)
        indent = n_leading_spaces(p)
        p_next_indent = 0 if i == len(perf) - 1 else n_leading_spaces(perf[i + 1])
        if last_indent >= indent:
            for _ in range(int((last_indent - indent) / N_INDENT + 1)):
                path.pop()
        if p_next_indent <= indent:
            f.write("{},{}\n".format("-".join(path + [n.name]), n.total_cycles))
        path.append(n.name)
        last_indent = indent