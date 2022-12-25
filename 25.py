with open('25.txt') as file:
    str1 = file.read()


# example
example_str = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''



# # un/comment this to toggle example (or follow-up example) vs actual data
# str1 = example_str




#########



lst1 = str1.split('\n')

def char_to_num(char):
    if (char == '2') or (char == '1') or (char == '0'):
        return int(char)
    if (char == '-'):
        return -1
    if (char == '='):
        return -2

lst2 = [[char_to_num(char) for char in strng] for strng in lst1]

print('lst2 is:', lst2)

# take "snafu" to mean a list whose elements are integers in [-2,2]

def snafu_to_decimal(lst):
    if len(lst) == 1:
        return lst[0]
    cpy = lst.copy()
    last = cpy.pop()
    return 5 * snafu_to_decimal(cpy) + snafu_to_decimal([last])

lst3 = [snafu_to_decimal(lst) for lst in lst2]

num = sum(lst3)

def decimal_to_quinary(num):
    if (num < 5):
        return [num]
    last = num % 5
    new = num // 5
    return decimal_to_quinary(new) + [last]

def quinary_to_snafu(lst):
    lst.reverse()
    for index, element in enumerate(lst):
        if element > 2:
            if index < len(lst) - 1:
                lst[index] -= 5
                lst[index+1] += 1
            else:
                lst[index] -= 5
                lst.append(1)
    lst.reverse()
    return lst

def decimal_to_snafu(num):
    return quinary_to_snafu(decimal_to_quinary(num))

snafu_as_lst = decimal_to_snafu(num)

def snafu_to_string(lst):
    def snafu_digit_to_char(digit):
        if digit >= 0:
            return str(digit)
        if digit == -1:
            return '-'
        if digit == -2:
            return '='
    return ''.join([snafu_digit_to_char(digit) for digit in lst])

snafu_answer = snafu_to_string(snafu_as_lst)


print('the answer to part 1 is:', snafu_answer)