with open('3.txt') as file:
    str = file.read()

lst_of_strs = str.split('\n')

def halve_str(string):
    L = len(string)
    H = round(L/2)
    return [string[0:H], string[H:]]

def common_char(pair):
    for char in pair[0]:
        if char in pair[1]:
            return char

def priority(char):
    if ord(char) < 91:
        return ord(char) - 38
    if ord(char) > 96:
        return ord(char) - 96

lst_of_pairs = [halve_str(entry) for entry in lst_of_strs]

lst_of_common_chars = [common_char(pair) for pair in lst_of_pairs]

lst_of_priorities = [priority(char) for char in lst_of_common_chars]

print('the answer to part 1 is:', sum(lst_of_priorities))


########################################


def group_by_three(lst):
    L = len(lst)
    T = round(L/3)
    output = []
    for i in range(T):
        output.append([lst[3*i], lst[3*i+1], lst[3*i+2]])
    return output
    
def three_common_char(triple):
    for char in triple[0]:
        if char in triple[1] and char in triple[2]:
            return char

lst_of_triples = group_by_three(lst_of_strs)

lst_of_ternary_common_chars = [three_common_char(triple) for triple in lst_of_triples]

lst_of_priorities_part_2 = [priority(char) for char in lst_of_ternary_common_chars]

print ('the answer to part 2 is:', sum(lst_of_priorities_part_2))