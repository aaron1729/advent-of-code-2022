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
# str1 = example_str



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

print('lst is', lst)


monkey_holdings = [sublst[0] for sublst in lst]

monkey_inspections = [0 for sublst in lst]




# key to part 2: a given monkey's behavior only depends on worry level modulo their modulus (in their test). however, we don't know where a given item will get thrown, so we need to keep track of the number relative to _all_ of their moduli. so, we should keep track of it modulo the LCM of their moduli.

import math
monkey_moduli = [sublst[2] for sublst in lst]

print('monkey_moduli is', monkey_moduli)

LCM = math.lcm(*monkey_moduli)

print('LCM of monkey_moduli is', LCM)





def round(monkey_holdings):
    for i in range(len(monkey_holdings)):
            # the exec function call below can't change a variable inside of a function unless it's passed the global dictionary (returned by `globals()`) as an optional argument indicating where this variable lives. but we apparently can't update that global variable from a local variable. so here, `old` is declared as a global variable so that `new` can be updated using it.
        # print('monkey number', i, 'is now inspecting.\n')
        monkey_inspections[i] += len(monkey_holdings[i])
        for num in monkey_holdings[i]:
            global old
            old = num
            # print('old worry level is', old)
            global new
            # print('instruction is', lst[i][1])
            exec(lst[i][1], globals())
            # print('new worry level is', new, '\n')
            # the following line is used for part 1, and removed for part 2.
            # new = new // 3
            new = new % LCM
            if (new % lst[i][2] == 0):
                monkey_holdings[lst[i][3]].append(new)
            else:
                monkey_holdings[lst[i][4]].append(new)
        monkey_holdings[i] = []
        # print('after monkey number', i, 'has gone, monkey_holdings is', monkey_holdings, '\n')
    return monkey_holdings

number_of_rounds = 10000

for i in range(number_of_rounds + 1):
    print('after', i, 'rounds, monkey_holdings is', monkey_holdings, 'and monkey_inspections is', monkey_inspections)
    if i < number_of_rounds:
        round(monkey_holdings)

copy_of_monkey_inspections = monkey_inspections.copy()

print(copy_of_monkey_inspections)

copy_of_monkey_inspections.sort(reverse = True)

print(copy_of_monkey_inspections)

print('level of monkey business after', number_of_rounds, 'rounds is', copy_of_monkey_inspections[0] * copy_of_monkey_inspections[1])