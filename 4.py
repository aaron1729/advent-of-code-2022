with open('4.txt') as file:
    str = file.read()

lst_of_strs = str.split('\n')

lst_of_pairs = [pair.split(',') for pair in lst_of_strs]

lst_of_pairs_of_bdries = [[pair[0].split('-'), pair[1].split('-')] for pair in lst_of_pairs]

lst_of_pairs_of_bdries_as_ints = [[[int(matrix[0][0]), int(matrix[0][1])], [int(matrix[1][0]), int(matrix[1][1])]] for matrix in lst_of_pairs_of_bdries]

def check_containment(matrix):
    if matrix[0][0] >= matrix[1][0] and matrix[0][1] <= matrix[1][1]:
        return True
    if matrix[0][0] <= matrix [1][0] and matrix[0][1] >= matrix[1][1]:
        return True
    return False

lst_of_containment_checks = [check_containment(matrix) for matrix in lst_of_pairs_of_bdries_as_ints]

print('sum for part 1 is:', sum(lst_of_containment_checks))

def check_overlap(matrix):
    if matrix[0][1] < matrix[1][0]:
        return False
    if matrix[1][1] < matrix[0][0]:
        return False
    return True

lst_of_overlap_checks = [check_overlap(matrix) for matrix in lst_of_pairs_of_bdries_as_ints]

print('sum for part 2 is:', sum(lst_of_overlap_checks))