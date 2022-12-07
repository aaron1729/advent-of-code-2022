with open('2.txt') as file:
    str = file.read()

lst_of_strs = str.split('\n')

def char_to_num(char):
    if char == 'A' or char == 'X':
        return 0
    if char == 'B' or char == 'Y':
        return 1
    if char == 'C' or char == 'Z':
        return 2

lst_of_pairs_of_nums = [[char_to_num(round[0]), char_to_num(round[2])] for round in lst_of_strs]

def part1(pair):
    shape_score = pair[1] + 1
    outcome_score = ((pair[1] - pair[0] + 1) % 3) * 3
    return shape_score + outcome_score

lst_of_points_part1 = [part1(pair) for pair in lst_of_pairs_of_nums]

print('part 1 score:', sum(lst_of_points_part1))

def part2(pair):
    outcome_score = pair[1] * 3
    shape_to_play = (pair[0] + pair[1] - 1) % 3
    shape_score = shape_to_play + 1
    return shape_score + outcome_score

lst_of_points_part2 = [part2(pair) for pair in lst_of_pairs_of_nums]

print('part 2 score:', sum(lst_of_points_part2))