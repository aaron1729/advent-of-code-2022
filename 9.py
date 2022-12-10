with open('9.txt') as file:
    str = file.read()

lst_of_numbered_instructions = str.split('\n')

lst_of_instructions_as_letters = []

for numbered_instruction in lst_of_numbered_instructions:
    direction = numbered_instruction[0]
    number = int(numbered_instruction[2:])
    for _ in range(number):
        lst_of_instructions_as_letters.append(direction)

def letter_to_coords(char):
    if char == 'U':
        return [0,1]
    if char == 'D':
        return [0,-1]
    if char == 'L':
        return [-1,0]
    if char == 'R':
        return [1,0]

lst_of_instructions = [letter_to_coords(letter) for letter in lst_of_instructions_as_letters]

head_pos = [0, 0]
tail_pos = [0, 0]

def new_tail_pos(head_pos, tail_pos):
    dx = head_pos[0] - tail_pos[0]
    dy = head_pos[1] - tail_pos[1]
    if dy == 0 and abs(dx) > 1:
        # below, the operator // denotes floor division, i.e. division without the remainder. the point is just that this outputs an integer rather than a floating-point number.
        tail_pos[0] += dx // abs(dx)
    if dx == 0 and abs(dy) > 1:
        tail_pos[1] += dy // abs(dy)
    if dx != 0 and dy != 0 and (abs(dx) > 1 or abs(dy) > 1):
        tail_pos[0] += dx // abs(dx)
        tail_pos[1] += dy // abs(dy)
    return tail_pos

visited_by_tail = [[0, 0]]

# here, use tuples because they're hashable (whereas lists aren't) so they can be 
visited_by_tail_dedupe = {(0, 0)}

for instruction in lst_of_instructions:
    head_pos[0] += instruction[0]
    head_pos[1] += instruction[1]
    tail_pos = new_tail_pos(head_pos, tail_pos)
    tail_pos_tuple = (tail_pos[0], tail_pos[1])
    # print('instruction is', instruction, 'and head is at', head_pos, 'and now tail pos is', tail_pos)
    visited_by_tail.append(tail_pos)
    visited_by_tail_dedupe.add(tail_pos_tuple)

# print('visited by tail is', visited_by_tail)

print('number of tail moves is', len(visited_by_tail))

print('number of locations visited by tail is', len(visited_by_tail_dedupe))