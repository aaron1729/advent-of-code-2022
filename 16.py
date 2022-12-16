with open('16.txt') as file:
    str1 = file.read()


# example
example_str = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''



# un/comment this to toggle example vs actual data
str1 = example_str



#########

lst1 = str1.split('\n')

lst = []

import re

for strng in lst1:
    sublst = []
    sublst.append(strng[6:8])
    start_rate = 23
    end_rate = re.search(";", strng).span()[0]
    sublst.append(int(strng[23:end_rate]))
    start_valves = re.search("valves* ", strng).span()[1]
    sublst.append(strng[start_valves:].split(", "))
    lst.append(sublst)
    

print('now lst is', lst)


