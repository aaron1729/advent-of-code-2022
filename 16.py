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




# # un/comment this to toggle example vs actual data
# str1 = example_str



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

# print('and now, essential_valves_dict is:', essential_valves_dict)

# # add back in 'AA' to essential_valves_dict, just to make things easy later.

essential_valves_dict_AA = {}
essential_valves_dict_AA["flow"] = 0
essential_valves_dict_AA["essential_targets"] = {}
for valve in essential_valves_dict:
    essential_valves_dict_AA["essential_targets"][valve] = min_dist('AA', valve)

essential_valves_dict["AA"] = essential_valves_dict_AA

# print('and now now, essential_valves_dict is:', essential_valves_dict)



# a route is recorded as a list of pairs. each pair contains a valve and a number saying at what minute the valve was opened. the numbers go in increasing order (i.e. the valves are listed in chronological order). all start with ('AA', 0), and valves never repeat.

# we build the routes recursively, and compare their high score against the current best. we do *not* actually record the routes, as there are 14! ~ 87billion of them.

# # in the given optimal solution for the example, valve DD is being opened in minute 2. thus, it is open at minutes 3, 4, 5, ..., 30, i.e. for 28 minutes. its flow rate is 20, so it releases 28 * 20 = 560 units of pressure. so in general, if a valve with flow rate F is being opened at minute M, then it releases (30-M) * F units of pressure.

def route_score(route):
    score = 0
    for (valve, time) in route:
        if time < 30:
            score += (30-time) * essential_valves_dict[valve]["flow"]
    return score

solution_to_example = [('AA', 0), ('DD, 2'), ('BB', 5), ('JJ', 9), ('HH', 17), ('EE', 21), ('CC', 24)]



high_score = 0
counter = 0

def make_routes(route=[('AA', 0)]):

    end_of_route = route[len(route)-1]
    current = end_of_route[0]
    time = end_of_route[1]
    
    if (time >= 30) or (len(route) == len(essential_valves_dict)):
        global counter
        counter += 1
        global high_score
        high_score = max(high_score, route_score(route))
        print('just found route number', counter, 'and now the new high score is', high_score)
        return
    
    for valve in essential_valves_dict[current]["essential_targets"]:
        visited_valves = [pair[0] for pair in route]
        if not valve in visited_valves:
            new_route = route.copy()
            new_route.append((valve, time + 1 + essential_valves_dict[current]["essential_targets"][valve]))
            make_routes(new_route)

make_routes()

print('high_score (the answer to part 1) is:', high_score)


######################################################