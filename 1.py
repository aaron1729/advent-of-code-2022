with open('1.txt') as file:
    str = file.read()

lst_of_strs = str.split('\n\n')

lst_of_lsts_of_strs = [f.split('\n') for f in lst_of_strs]

lst_of_lsts_of_nums = [[int(numstr) for numstr in lst_of_strs] for lst_of_strs in lst_of_lsts_of_strs]

lst_of_sums = [sum(lst_of_nums) for lst_of_nums in lst_of_lsts_of_nums]

lst_of_sums.sort(reverse=True)

print('max value is:', lst_of_sums[0])

sum_of_top_three = sum(lst_of_sums[0:3])

print('sum of top three values is:', sum_of_top_three)