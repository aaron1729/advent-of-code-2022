with open('13.txt') as file:
    str1 = file.read()


# example
example_str = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''


# # un/comment this to toggle example vs actual data
# str1 = example_str


#########


lst1 = str1.split('\n\n')

lst2 = [substr.split('\n') for substr in lst1]

import ast

lst3 = [[ast.literal_eval(sublst[0]), ast.literal_eval(sublst[1])] for sublst in lst2]

# print(lst3)

# keep a list as-is, but turn an integer into a one-element list
def listify(input):
    if isinstance(input, int):
        return [input]
    else:
        return input

# return boolean recording whether they are in the correct order (left < right)
def compare(left, right):
    L = min(len(left), len(right))
    for i in range(L):
        # print('checking pair number', i)
        if isinstance(left[i], int) and isinstance(right[i], int):
            # print('compare', left[i], 'vs', right[i])
            if left[i] < right[i]:
                # print('inside here')
                return True
            if left[i] > right[i]:
                # print('inside there')
                return False
        else:
            possible_output = compare(listify(left[i]), listify(right[i]))
            if isinstance(possible_output, bool):
                return possible_output
    if len(right) > L:
        return True
    if len(left) > L:
        return False


answer_part_1 = 0

for i, pair in enumerate(lst3):
    if compare(pair[0], pair[1]):
        answer_part_1 += i + 1

print('answer to part 1 is', answer_part_1)

### part 2

lst4 = []

for pair in lst3:
    lst4 += pair

divider1 = [[2]]
divider2 = [[6]]

lst4 += [divider1, divider2]

# print('lst4 is', lst4)

# bubblesort
    # i is the index of the round of bubblesorting
    # j is the index of the earlier element of the pair getting compared and possibly swapped
# for bubblesorting with L elements:
    # the 0th round has L-1 comparisons, so j ranges from 0 to L-2.
    # the 1st round has L-2 comparisons, so j ranges from 0 to L-3.
    # in general, the i'th round has L-i-1 comparisons, so j ranges from 0 to L-i-2, i.e. it's drawn from range(L-i-1).
    # altogether, there are L-1 rounds, so i ranges from 0 to L-2, i.e. it's drawn from range(L-1).
for i in range(len(lst4)-1):
    for j in range(len(lst4)-i-1):
        if not compare(lst4[j], lst4[j+1]):
            temp = lst4[j+1]
            lst4[j+1] = lst4[j]
            lst4[j] = temp

# print('after bubblesorting, lst4 is', lst4)


location1 = None
location2 = None

for i, packet in enumerate(lst4):
    if packet == divider1:
        location1 = i
    if packet == divider2:
        location2 = i

print('answer to part 2 is', (location1 + 1) * (location2 + 1))