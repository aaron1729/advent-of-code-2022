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

# print('and now now, essential_valves_dict is:', essential_valves_dict)


essential_valves = list(essential_valves_dict.keys())

essential_valves.remove('AA')

print('the list essential_valves is:', essential_valves)

# a route is recorded as a list of pairs. each pair contains a valve and a number saying at what minute the valve was opened. the numbers go in increasing order (i.e. the valves are listed in chronological order). all start with ('AA', 0), and valves never repeat.

# we build the routes recursively, and compare their high score against the current best. we do *not* actually record the routes, as there are 14! ~ 87billion of them.

# # in the given optimal solution for the example, valve DD is being opened in minute 2. thus, it is open at minutes 3, 4, 5, ..., 30, i.e. for 28 minutes. its flow rate is 20, so it releases 28 * 20 = 560 units of pressure. so in general, if a valve with flow rate F is being opened at minute M, then it releases (30-M) * F units of pressure.

total_time = 30

def route_score(route):
    score = 0
    for (valve, time) in route:
        global total_time
        if time < total_time:
            score += (total_time-time) * essential_valves_dict[valve]["flow"]
    return score

solution_to_example = [('AA', 0), ('DD, 2'), ('BB', 5), ('JJ', 9), ('HH', 17), ('EE', 21), ('CC', 24)]



high_score = 0
counter = 0



def make_routes(route=[('AA', 0)], allowed_essential_valves=essential_valves):

    end_of_route = route[len(route)-1]
    current = end_of_route[0]
    time = end_of_route[1]
    
    # below, the +1 at the end is to account for the starting 'AA'
    global total_time
    if (time >= total_time) or (len(route) == len(allowed_essential_valves) + 1):
        global counter
        counter += 1
        global high_score
        high_score = max(high_score, route_score(route))
        print('just found route number', counter, 'and now the new high score is', high_score)
        return
    
    visited_valves = [pair[0] for pair in route]

    for valve in allowed_essential_valves:
        if not valve in visited_valves:
            new_route = route.copy()
            new_route.append((valve, time + 1 + essential_valves_dict[current]["essential_targets"][valve]))
            make_routes(new_route)


# # run the following function and print statement to solve part 1
# make_routes()
# print('the answer to part 1 is:', high_score) # 1418 for the actual input data, 1651 for the example data


######################################################

# for part 2, use the same functions but with a different total_time:
total_time = 26

# idea: all that matters are the person and elephant's individual routes -- and in fact it doesn't matter which is whose. so, look at the set of disjoint union decompositions of the set of essential nodes (not counting the starting point 'AA'); for each decomposition S0 \sqcup S1, find the best score for S0 and S1 individually, and sum these to get the best possible total score given this decomposition.

# with N essential valve, there are 2^N decompositions, and 2^N/2 = 2^{N-1} if we don't care which subset is whose. these are respectively in bijection with N-digit binary strings and those that start with 0 (i.e. (N-1)-digit binary strings). (said differently, WLOG we can pin "0" to be the target of the first essential valve.)

def powerset(lst):
    if len(lst) == 0:
        return [[]]
    shorter = lst.copy()
    last = shorter.pop()
    powerset_of_shorter = powerset(shorter)
    return powerset_of_shorter + [subset + [last] for subset in powerset_of_shorter]

essential_valves_powerset = powerset(essential_valves)

# print('essential_valves_powerset is:', essential_valves_powerset)

essential_valves_powerset_complements = []
for subset in essential_valves_powerset:
    complement = essential_valves.copy()
    for element in subset:
        complement.remove(element)
    essential_valves_powerset_complements.append(complement)

print('length of essential_valves:', len(essential_valves))
print('length of powerset:', len(essential_valves_powerset))



high_scores_2 = []

# divide by two WLOG, since roles are interchangeable
for i in range(len(essential_valves_powerset) // 2):

    print('now i is', i)
    
    high_score = 0
    counter = 0
    make_routes(allowed_essential_valves=essential_valves_powerset[i])
    high_score_0 = high_score

    high_score = 0
    counter = 0
    make_routes(allowed_essential_valves=essential_valves_powerset_complements[i])
    high_score_1 = high_score

    high_scores_2.append([high_score_0, high_score_1, high_score_0 + high_score_1])


print('high_scores_2 is:', high_scores_2)

# print('solution to part 2 is:', max([triple[2] for triple in high_scores_2]))





























####################################################################################################################################

# the stuff below here is old, and probably worthless.



#### score the two routes.

def route_score2(route):
    score = 0
    for (valve, time) in route:
        if time < 26:
            score += (26-time) * essential_valves_dict[valve]["flow"]
    return score



high_score2 = 0
counter2 = 0

# as in part 1, this runs via recursion for both of them continuing to take steps. however, now we must be more careful: we want to only take those steps that stay *within* the time bounds. otherwise, we might occupy a valve valuelessly on one route, obstructing the other from incorporating it valuefully.
def make_2_routes(route0=[('AA', 0)], route1=[('AA', 0)]):

    end_of_route0 = route0[len(route0)-1]
    current0 = end_of_route0[0]
    time0 = end_of_route0[1]

    end_of_route1 = route1[len(route1)-1]
    current1 = end_of_route1[0]
    time1 = end_of_route1[1]

    # here, the +1 at the end is because route0 and route1 share the starting valve 'AA' (but they are otherwise disjoint).
    if ((time0 >= 26) and (time1 >= 26)) or (len(route0) + len(route1) == len(essential_valves_dict) + 1):
        global counter2
        counter2 += 1
        global high_score2
        high_score2 = max(high_score2, route_score2(route0) + route_score2(route1))
        print('just found completed route-pair number', counter2, 'and now the new high score is', high_score2)
        return

    visited_valves = [pair[0] for pair in route0] + [pair[0] for pair in route1]

    # extend route0 and call the function recusively
    for valve in essential_valves_dict[current0]["essential_targets"]:
        # print('thinking about adding', valve, 'to route0')
        if not valve in visited_valves:
            # print('adding', valve, 'to route0')
            new_route0 = route0.copy()
            new_time0 = time0 + 1 + essential_valves_dict[current0]["essential_targets"][valve]
            if new_time0 < 26:
                new_route0.append((valve, new_time0))
                print('now route0 is:', new_route0)
                print('while route1 remains', route1)
                make_2_routes(new_route0, route1)
    
    # extend route1 and call the function recusively
    for valve in essential_valves_dict[current1]["essential_targets"]:
        # print('thinking about adding', valve, 'to route1')
        if not valve in visited_valves:
            # print('adding', valve, 'to route1')
            new_route1 = route1.copy()
            new_time1 = time1 + 1 + essential_valves_dict[current1]["essential_targets"][valve]
            if new_time1 < 26:
                new_route1.append((valve, new_time1))
                print('now route1 is:', new_route1)
                print('while route0 remains', route0)
                make_2_routes(route0, new_route1)

# # run the following function and print statement to solve part 2
# make_2_routes()
# print('answer to part 2 is:', high_score2)