with open('8.txt') as file:
    str = file.read()

# this is the example given 
# str = '30373\n25512\n65332\n33549\n35390'

lines = str.split('\n')

digits = [[int(one_char_string) for one_char_string in list(line)] for line in lines]

height = len(digits)
width = len(digits[0])

print('height of array is:', height)
print('width of array is:', width)


## for part 1: check if a tree is visible from outside from each direction

digits_and_bools = [[[digit, []] for digit in line] for line in digits]

# from north
for i in range(width):
    curr_max = -1
    for j in range(height):
        pointer = digits_and_bools[j][i]
        if pointer[0] > curr_max:
            pointer[1].append(True)
            curr_max = pointer[0]
        else:
            pointer[1].append(False)

# from east
for i in range(height):
    curr_max = -1
    for j in range(width):
        pointer = digits_and_bools[i][width-j-1]
        if pointer[0] > curr_max:
            pointer[1].append(True)
            curr_max = pointer[0]
        else:
            pointer[1].append(False)

# from south
for i in range(width):
    curr_max = -1
    for j in range(height):
        pointer = digits_and_bools[height-j-1][i]
        if pointer[0] > curr_max:
            pointer[1].append(True)
            curr_max = pointer[0]
        else:
            pointer[1].append(False)

# from west
for i in range(height):
    curr_max = -1
    for j in range(width):
        pointer = digits_and_bools[i][j]
        if pointer[0] > curr_max:
            pointer[1].append(True)
            curr_max = pointer[0]
        else:
            pointer[1].append(False)

# a logical-OR reducer
def reduce_bools(lst):
    for bool in lst:
        if bool == True:
            return True
    return False

digits_and_reduced_bools = [[[pair[0], reduce_bools(pair[1])] for pair in line] for line in digits_and_bools]

reduced_bools = [[pair[1] for pair in line] for line in digits_and_reduced_bools]

line_sums = [sum(line) for line in reduced_bools]

print('answer to part 1 is:', sum(line_sums))

## for part 2: check how far one can see from a given tree in each direction

digits_and_distances = [[[digit, []] for digit in line] for line in digits]

# given an input height N and a list of numbers, count the length of the list once it's been truncated *after* the first instance of a number N or above
def count(N, lst):
    counter = 0
    for num in lst:
        if num < N:
            counter += 1
        else:
            counter += 1
            return counter
    return counter

# facing north
for i in range(width):
    for j in range(height):
        pointer = digits_and_distances[j][i]
        N = pointer[0]
        lst = [line[i] for line in digits[0:j]]
        lst.reverse()
        pointer[1].append(count(N, lst))

# facing east
for i in range(height):
    for j in range(width):
        pointer = digits_and_distances[i][j]
        N = pointer[0]
        lst = digits[i][j+1:]
        pointer[1].append(count(N, lst))

# facing south
for i in range(width):
    for j in range(height):
        pointer = digits_and_distances[j][i]
        N = pointer[0]
        lst = [line[i] for line in digits[j+1:]]
        pointer[1].append(count(N, lst))

# facing west
for i in range(height):
    for j in range(width):
        pointer = digits_and_distances[i][j]
        N = pointer[0]
        lst = digits[i][0:j]
        lst.reverse()
        pointer[1].append(count(N, lst))

# a multiplication reducer
def reduce_nums(lst):
    output = 1
    for num in lst:
        output *= num
    return output

digits_and_scenic_scores = [[[pair[0], reduce_nums(pair[1])] for pair in line] for line in digits_and_distances]

line_maxima = [max([pair[1] for pair in line]) for line in digits_and_scenic_scores]

print('answer to part 2 is:', max(line_maxima))