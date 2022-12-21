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

# the first item in this list will be: ['AA', 0, ['DD', 'II', 'BB']]
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

# print('valves_dict is:', valves_dict)


# only keep track of "essential" valves: those with positive flow rate. also keep track of the distances between them. (minimal routes will generally pass through multiple tunnels.) to do so, "targets" will now be a *dictionary* consisting of targets and their distances.

essential_valves_dict = {}

for valve in valves_dict:
    if valves_dict[valve]["flow"] > 0:
        essential_valves_dict[valve] = valves_dict[valve]

# print('essential_valves_dict is:', essential_valves_dict)



import math

# find minimum distance between any two valves
def min_dist(start, end):

    # copy the dictionary, so as not to modify the original
    cpy = valves_dict.copy()
    unvisited = set(valve for valve in cpy)
    
    # set "minimum known distances" to infinity, except 0 for the start
    for valve in cpy:
        cpy[valve]["dist_from_start"] = math.inf
    cpy[start]["dist_from_start"] = 0
    
    # run dijkstra
    current = start
    while True:
        for valve in valves_dict[current]["targets"]:
            if valve in unvisited:
                # print('valve is unvisited, and it is:', valve)
                cpy[valve]["dist_from_start"] = min(cpy[valve]["dist_from_start"], 1+cpy[current]["dist_from_start"])
                # print('and its new minimum known distance is:', cpy[valve]["dist_from_start"])
        unvisited.remove(current)
        unvisited_pairs = {(valve, cpy[valve]["dist_from_start"]) for valve in unvisited}
        # print('the set of unvisited pairs is:', unvisited_pairs)
        min_dist_among_unvisited = min(pair[1] for pair in unvisited_pairs)
        # print('and minimum distance among unvisited pairs is:', min_dist_among_unvisited)
        for pair in unvisited_pairs:
            if pair[1] == min_dist_among_unvisited:
                current = pair[0]
                break
        if current == end:
            return cpy[end]["dist_from_start"]

for valve in essential_valves_dict:
    essential_valves_dict[valve]["essential_targets"] = {}
    # del essential_valves_dict[valve]["targets"]
    for essential_target in essential_valves_dict:
        if essential_target != valve:
            essential_valves_dict[valve]["essential_targets"][essential_target] = min_dist(valve, essential_target)

print('and now, essential_valves_dict is:', essential_valves_dict)

# add back in 'AA' to essential_valves_dict, just to make things easy later.

essential_valves_dict_AA = {}
essential_valves_dict_AA["flow"] = 0
essential_valves_dict_AA["essential_targets"] = {}
for valve in essential_valves_dict:
    essential_valves_dict_AA["essential_targets"][valve] = min_dist('AA', valve)

essential_valves_dict["AA"] = essential_valves_dict_AA

print('and now now, essential_valves_dict is:', essential_valves_dict)






########################################################










flows = [sublst[1] for sublst in lst]

max_flow = max(flows)

print('max_flow is:', max_flow)

flows_sorted = flows.copy()

flows_sorted.sort(reverse=True)

print('flows_sorted is', flows_sorted)

flows_sorted_filtered = list(filter(lambda flow: flow > 0, flows_sorted))

print('flows_sorted_filtered is', flows_sorted_filtered)

max_remaining_points_possible = []

for i in range(30):
    L = min(30-i, len(flows_sorted_filtered))
    output = 0
    for j in range(L):
        output += flows_sorted_filtered[j] * (30-i-j)
    max_remaining_points_possible.append(output)

print('max_remaining_points_possible is', max_remaining_points_possible)



# create all routes of length N, for N running from 1 to 30. at each stage, find the maximum score thus far, and the maximum number of points possible for the remainder of the time, and throw away all of the routes that have no chance of being optimal.

# a route is recorded as a list of pairs. each pair contains a valve and a boolean. the boolean records whether we are *currently* opening the valve.

base_route = [('AA', False)]

def score(route):
    output = 0
    for index, pair in enumerate(route):
        if pair[1]:
            output += valves_dict[pair[0]]["flow"] * (30 - index)
    return output


### these are from the example input, not the real input. so they must be commented out when running the code for real.

# example_route_1 = [('AA', False), ('AA', True), ('DD', False), ('DD', True)]
# print('score of example_route_1 is:', score(example_route_1)) # 540

# example_route_2 = [('AA', False), ('AA', True), ('DD', False), ('CC', False)]
# print('score of example_route_2 is:', score(example_route_2)) # 0

# example_route_3 = [('AA', False), ('DD', False), ('DD', True), ('CC', False)]
# print('score of example_route_3 is:', score(example_route_3)) # 560
# # this is how the given optimal solution in the example begins. the DD valve is open at minutes 3, 4, 5, ..., 30, i.e. for 28 minutes. its flow rate is 20, so it releases 28 * 20 = 560 units of pressure. so this is correct! (not off by one.)





routes = [base_route]

essentially_complete_routes = []

high_score = 0

# a complete route has length 31. (it starts with ('AA', False) at minute 0.)
    # after 0 iterations (i.e. iterating through range(0)), every route in the routes list has length 1.
    # after 1 iteration (i.e. iterating through range(1)), every route in the routes list has length 2.
    # etc.
# so, we want to iterate through range(30).
for i in range(0):
    new_routes = []
    for route in routes:
        # print('extending the route:', route)
        last = route[len(route)-1]
        opened = [pair[0] for pair in route if pair[1]]
        # if the flow rate of a given valve is 0, it cannot strictly improve the score to open the valve. so, only open the valves with positive flow rate.
        if (not last[0] in opened) and (valves_dict[last[0]]["flow"] > 0):
            new_routes.append(route + [(last[0], True)])
        for valve in valves_dict[last[0]]["targets"]:
            new_routes.append(route + [(valve, False)])
    scores = [score(route) for route in new_routes]
    high_score = max(max(scores), high_score)
    new_viable_routes = []
    for j in range(len(new_routes)):
        if scores[j] + max_remaining_points_possible[i] >= high_score:
            new_viable_routes.append(new_routes[j])
    routes = []
    for route in new_viable_routes:
        opened = [pair[0] for pair in route if pair[1]]
        if len(opened) >= len(flows_sorted_filtered):
            essentially_complete_routes.append(route)
        else:
            routes.append(route)

    print('at the end of iteration numbered', i, 'of the for loop (starting with 0), routes has length', len(routes))
    print('and essentially_complete_routes has length', len(essentially_complete_routes))
    # print('and their scores are', [score(route) for route in routes])
    print('and each route has length', len(routes[0]))
    print('and the maximum score so far is', high_score)
    print('and we threw away', len(new_routes) - len(new_viable_routes), 'routes because they were not viable')
    print('\n')










# run through all possible sequences of actions, and add them to a list of routes. each sequence of actions is recorded as a list of 3-tuples containing the valve name, pressure, and time of opening.
routes = []


# the list "output" contains pairs of a valve and a boolean indicating whether we're currently opening it.
# the set "opened" records (locally!) whether a valve has been opened in a given route, as we're constructing it.
def create_routes(current='AA', output=[('AA', False)], opened=set()):
    # print('currently, length of output is:', len(output))
    if len(output) == 3:
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

# create_routes()

# print('after create_routes, routes length is:', len(routes))
