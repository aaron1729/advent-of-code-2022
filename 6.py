import copy

with open('6.txt') as file:
    str = file.read()

def unique(lst):
    for i in range(len(lst)):
        for j in [k+i+1 for k in range(len(lst)-i-1)]:
            if lst[i] == lst[j]:
                return False
    return True

def process(L, string):
    lst = []
    for n in range(L):
        lst.append(string[n])
    for n in [m+L for m in range(len(string)-L)]:
        if unique(lst):
            return n
        lst.pop(0)
        lst.append(string[n])
    return False



print(process(4, 'bvwbjplbgvbhsrlpgdmjqwftvncz')) # gives 5, as expected

print(process(4, 'nppdvjthqldpwncqszvftbrmjlhg')) # gives 6, as expected

print(process(4, 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')) # gives 10, as expected

print(process(4, 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')) # gives 11, as expected

#print('answer to part 1 is:', process4(str))

print('answer to part 1 is:', process(4, str))

print('answer to part 2 is:', process(14, str))

