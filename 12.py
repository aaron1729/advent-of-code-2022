with open('12.txt') as file:
    str1 = file.read()


# example
example_str = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''


# # un/comment this to toggle example vs actual data
# str1 = example_str


#########

lst1 = str1.split('\n')

# typecast a string into a list
lst2 = [list(string) for string in lst1]
# print('originally, lst2 is', lst2)

S = None
E = None

for (index, sublst) in enumerate(lst2):
    for (subindex, char) in enumerate(sublst):
        if char == 'S':
            S = (index, subindex)
            sublst[subindex] = 'a'
        if char == 'E':
            E = (index, subindex)
            sublst[subindex] = 'z'

print('S is', S)
print('E is', E)
# print('now, lst2 is', lst2)
print('just for context, the function ord takes the following values:')
print('ord(a) is', ord('a'))
print('ord(b) is', ord('b'))
print('ord(c) is', ord('c'))
print('ord(S) is', ord('S'))
print('ord(E) is', ord('E'))

lst3 = [[ord(char) for char in sublst] for sublst in lst2]

import math

### part 1

# each triple records the height, the "visited yet" boolean, and the minimum known distance to that node.
dijkstra1 = [[[num, False, math.inf] for num in sublst] for sublst in lst3]

dijkstra1[S[0]][S[1]][2] = 0

found_E = False
current = S

while not found_E:
    height_current = dijkstra1[current[0]][current[1]][0]
    Deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for Delta in Deltas:
        new = tuple(map(sum, zip(current, Delta)))
        # make sure new is on the grid:
        if new[0] >= 0 and new[0] < len(dijkstra1) and new[1] >= 0 and new[1] < len(dijkstra1[0]):
            # make sure we can walk to new
            height_new = dijkstra1[new[0]][new[1]][0]
            if (height_new - height_current <= 1):
                # make sure new is unvisited:
                if not dijkstra1[new[0]][new[1]][1]:
                    # set its tentative distance
                    dijkstra1[new[0]][new[1]][2] = dijkstra1[current[0]][current[1]][2] + 1
    dijkstra1[current[0]][current[1]][1] = True
    # find an unvisited node with minimum known distance. (there may be many of these, but just choose the first one.)
    the_min_data = [math.inf, None, None]
    for i, row in enumerate(dijkstra1):
        for j, node in enumerate(row):
            if (not node[1]) and (node[2] < the_min_data[0]):
                the_min_data = [node[2], i, j]
    current = (the_min_data[1], the_min_data[2])
    if current == E:
        print('found E, and its distance is', dijkstra1[E[0]][E[1]][2])











