with open('14.txt') as file:
    str1 = file.read()


# example
example_str = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''


# # un/comment this to toggle example vs actual data
# str1 = example_str


#########

lst1 = str1.split('\n')

lst2 = [strng.split(' -> ') for strng in lst1]

lst3 = [[strng.split(',') for strng in sublst] for sublst in lst2]

lst = [[tuple([int(strng) for strng in pair]) for pair in sublst] for sublst in lst3]

print('lst is', lst[0])

lst_x = [[pair[0] for pair in sublst] for sublst in lst]

lst_y = [[pair[1] for pair in sublst] for sublst in lst]

pathwise_min_x = [min(sublst) for sublst in lst_x]
min_x = min(pathwise_min_x)
pathwise_max_x = [max(sublst) for sublst in lst_x]
max_x = max(pathwise_max_x)
pathwise_min_y = [min(sublst) for sublst in lst_y]
min_y = min(pathwise_min_y)
pathwise_max_y = [max(sublst) for sublst in lst_y]
max_y = max(pathwise_max_y)

print('x bounds are', min_x, 'and', max_x)

print('y bounds are', min_y, 'and', max_y)

print('max_y is', max_y)

# print('x bounds are', min(min(lst_x)), 'and', max(max(lst_x)))

# print('y bounds are', min(min(lst_y)), 'and', max(max(lst_y)))

print('minimum length path has', min([len(path) for path in lst]), 'points')



### part 1

# this function takes in two 2-element tuples -- (x,y)-coordinates -- which are either horizontally or vertically aligned, and returns a list of the tuples comprising the closed interval between them.
def straight_line(pair0, pair1):
    Delta = (0,0)
    if (pair0[0] == pair1[0]) and (pair0[1] != pair1[1]):
        dy = pair1[1] - pair0[1]
        Delta = (0, dy // abs(dy))
    if (pair0[0] != pair1[0]) and (pair0[1] == pair1[1]):
        dx = pair1[0] - pair0[0]
        Delta = (dx // abs(dx), 0)
    output = [pair0]
    current = pair0
    while current != pair1:
        current = tuple(map(sum, zip(current, Delta)))
        output.append(current)
    return output

blocks1 = set()

for path in lst:
    for i in range(len(path)-1):
        segment = straight_line(path[i], path[i+1])
        for pair in straight_line(path[i], path[i+1]):
            blocks1.add(pair)

# save for later
blocks2 = blocks1.copy()

counter1 = 0
fell_into_abyss = False
initial = (500, 0)
current = initial

while not fell_into_abyss:
    down = tuple(map(sum, zip(current, (0, 1))))
    down_left = tuple(map(sum, zip(current, (-1, 1))))
    down_right = tuple(map(sum, zip(current, (1, 1))))
    if down not in blocks1:
        current = down
    else:
        if down_left not in blocks1:
            current = down_left
        else:
            if down_right not in blocks1:
                current = down_right
            else:
                counter1 += 1
                blocks1.add(current)
                current = initial
    if current[1] > max_y:
        fell_into_abyss = True

print('counter1 is', counter1)



### part 2

# obviously don't literally add an infinite line. rather, the worst-case scenario is that a block moves only down-left or only down-right. so the x-coordinates can start at 500-(max_y+2) and end at 500+(max_y+2), give or take.

for i in range(2 * max_y + 10):
    blocks2.add((500-max_y-5+i, max_y+2))

counter2 = 0
source_blocked = False
initial = (500, 0)
current = initial

while not source_blocked:
    down = tuple(map(sum, zip(current, (0, 1))))
    down_left = tuple(map(sum, zip(current, (-1, 1))))
    down_right = tuple(map(sum, zip(current, (1, 1))))
    if down not in blocks2:
        current = down
    else:
        if down_left not in blocks2:
            current = down_left
        else:
            if down_right not in blocks2:
                current = down_right
            else:
                counter2 += 1
                blocks2.add(current)
                if current == (500, 0):
                    source_blocked = True
                current = initial

print('counter2 is', counter2)
