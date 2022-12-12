with open('11.txt') as file:
    str1 = file.read()


# example
example_str = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

# un/comment this to toggle example vs actual data
str1 = example_str



#########



lst1 = str1.split('\n\n')

# print('lst1 is', lst1)

lst2 = [line.split('\n') for line in lst1]

def lines_to_data(lst):
    output = []
    output.append([int(numstr) for numstr in lst[1][18:].split(', ')])
    output.append(lst[2][13:])
    output.append(int(lst[3][21:]))
    output.append(int(lst[4][29:]))
    output.append(int(lst[5][30:]))
    return(output)



# this contains just the relevant data from the input text
lst = [lines_to_data(lst) for lst in lst2]

monkey_holdings = [lst[0] for lst in lst]

def round(monkey_holdings):
    for i in range(len(monkey_holdings)):
        for num in monkey_holdings[i]:
            global old
            old = num
            # print('old is', old)
            # print('num is', num)
            new = None
            exec(lst[i][1], globals())
            # print('now new is', new)





round(monkey_holdings)
