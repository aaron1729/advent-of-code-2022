with open('10.txt') as file:
    str = file.read()



# # this is the very short example
# str = '''noop
# addx 3
# addx -5'''


# # this is the longer example
# str = '''addx 15
# addx -11
# addx 6
# addx -3
# addx 5
# addx -1
# addx -8
# addx 13
# addx 4
# noop
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx -35
# addx 1
# addx 24
# addx -19
# addx 1
# addx 16
# addx -11
# noop
# noop
# addx 21
# addx -15
# noop
# noop
# addx -3
# addx 9
# addx 1
# addx -3
# addx 8
# addx 1
# addx 5
# noop
# noop
# noop
# noop
# noop
# addx -36
# noop
# addx 1
# addx 7
# noop
# noop
# noop
# addx 2
# addx 6
# noop
# noop
# noop
# noop
# noop
# addx 1
# noop
# noop
# addx 7
# addx 1
# noop
# addx -13
# addx 13
# addx 7
# noop
# addx 1
# addx -33
# noop
# noop
# noop
# addx 2
# noop
# noop
# noop
# addx 8
# noop
# addx -1
# addx 2
# addx 1
# noop
# addx 17
# addx -9
# addx 1
# addx 1
# addx -3
# addx 11
# noop
# noop
# addx 1
# noop
# addx 1
# noop
# noop
# addx -13
# addx -19
# addx 1
# addx 3
# addx 26
# addx -30
# addx 12
# addx -1
# addx 3
# addx 1
# noop
# noop
# noop
# addx -9
# addx 18
# addx 1
# addx 2
# noop
# noop
# addx 9
# noop
# noop
# noop
# addx -1
# addx 2
# addx -37
# addx 1
# addx 3
# noop
# addx 15
# addx -21
# addx 22
# addx -6
# addx 1
# noop
# addx 2
# addx 1
# noop
# addx -10
# noop
# noop
# addx 20
# addx 1
# addx 2
# addx 2
# addx -6
# addx -11
# noop
# noop
# noop'''






lines = str.split('\n')

summands = [1]

for line in lines:
    if line == "noop":
        summands.append(0)
    if line[0:4] == "addx":
        summands.append(0)
        summands.append(int(line[5:]))

# partial_sums[n] is the value of X during the (n+1)'st cycle. said differently, the value of X during the n'th cycle is partial_sums[n-1].
partial_sums = [sum(summands[0:n+1]) for n in range(len(summands))]

lst_1 = []
for i in range(6):
    lst_1.append(partial_sums[19 + 40 * i] * (20 + 40 * i))

print('answer to part 1 is', sum(lst_1))

pixels = []

# here, n (mod 40) represents the horizontal position of the CRT during the (n+1)'st cycle, e.g. it draws the pixel in position 0 during cycle 1. so, n % 40 must be compared with partial_sums[n].
for n in range(40 * 6):
    if (abs((n % 40) - partial_sums[n])) <= 1:
        pixels.append('#')
    else:
        pixels.append(' ')

pixel_strs = []
for i in range(6):
    str = ''
    for j in range(40):
        str += pixels[40*i + j]
    pixel_strs.append(str)
    
print('answer to part 2 is:')
for i in range(6):
    print(pixel_strs[i])

# BPJAZGAP