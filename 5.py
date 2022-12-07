import copy

with open('5.txt') as file:
    str = file.read()

lst_of_strs = str.split('\n')

### make the initial configuration: a list of lists

config1 = lst_of_strs[:8]

config2 = [[line[1], line[5], line[9], line[13], line[17], line[21], line[25], line[29], line[33]] for line in config1]

config2.reverse()

config3 = [[] for _ in range(9)]

for lst in config2:
    for n in range(9):
        if lst[n] != ' ':
            config3[n].append(lst[n])

config_part1 = copy.deepcopy(config3)

config_part2 = copy.deepcopy(config3)

### make the instructions: a list of triples of numbers

instructions1 = lst_of_strs[10:]

instructions2 = [str.split(' ') for str in instructions1]

# note zero-indexing
instructions3 = [[int(lst[1]), int(lst[3])-1, int(lst[5])-1] for lst in instructions2]

instructions = instructions3

def do_part1(conf, instruction):
    source = instruction[1]
    target = instruction[2]
    for _ in range(instruction[0]):
        conf[target].append(conf[source].pop())

for instruction in instructions:
    do_part1(config_part1, instruction)

answer_part1 = ''

for lst in config_part1:
    answer_part1 += lst.pop()

print('part 1 answer is:', answer_part1)

def do_part2(conf, instruction):
    source = instruction[1]
    target = instruction[2]
    chunk = conf[source][-instruction[0]:]
    conf[source] = conf[source][:-instruction[0]]
    conf[target] += chunk

for instruction in instructions:
    do_part2(config_part2, instruction)

answer_part2 = ''

for lst in config_part2:
    answer_part2 += lst.pop()

print('part 2 answer is:', answer_part2)