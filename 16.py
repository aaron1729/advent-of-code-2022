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


# print('now lst is', lst)




valves_dict = {}

for sublst in lst:
    valves_dict[sublst[0]] = {"flow": sublst[1], "targets": sublst[2]}

print('valves_dict is:', valves_dict)





# run through all possible sequences of actions, and add them to a list of routes. each sequence of actions is recorded as a list of 3-tuples containing the valve name, pressure, and time of opening.
routes = []


# the list "output" contains pairs of a valve and a boolean indicating whether we're sticking around to open it.
# the set "opened" records *locally* whether a valve has been opened in a given route, as we're constructing it.
def create_routes(current='AA', output=[('AA', False)], opened=set()):
    # print('currently, length of output is:', len(output))
    if len(output) == 2:
        routes.append(output)
        print('just added to routes, and and now its length is:', len(routes))
        print('and the route added is:', output)
        return

    last = output[len(output)-1][0]
    if not (last in opened):
        new_opened = opened.copy()
        new_opened.add(last)
        create_routes(last, output + [(last, True)], new_opened)

    for valve in valves_dict[last]["targets"]:
        # fork off into different versions of the "output" list.
        # print('forking off into different tunnels, and currently output is:', output)
        create_routes(valve, output + [(valve, False)], opened)

create_routes()

print('after create_routes, routes length is:', len(routes))
