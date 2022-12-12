with open('12.txt') as file:
    str1 = file.read()


# example
example_str = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''


# # un/comment this to toggle example vs actual data
# str1 = example_str


#########

lst1 = str1.split('\n')

# typecast a string into a list
lst2 = [list(string) for string in lst1]
# print('originally, lst2 is', lst2)

S = None
E = None

for (index, sublst) in enumerate(lst2):
    for (subindex, char) in enumerate(sublst):
        if char == 'S':
            S = (index, subindex)
            sublst[subindex] = 'a'
        if char == 'E':
            E = (index, subindex)
            sublst[subindex] = 'z'

print('S is', S)
print('E is', E)
# print('now, lst2 is', lst2)
print('just for context, the function ord takes the following values:')
print('ord(a) is', ord('a'))
print('ord(b) is', ord('b'))
print('ord(c) is', ord('c'))
print('ord(S) is', ord('S'))
print('ord(E) is', ord('E'))

lst3 = [[ord(char) for char in sublst] for sublst in lst2]

# print('lst3 is', lst3)

###

routes = []

def walk(history):
    current = history[len(history)-1]
    height_current = lst3[current[0]][current[1]]
    Deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for Delta in Deltas:
        # make a copy of the history so we're not affecting the original version
        history_copy = history.copy()
        new = tuple(map(sum, zip(current, Delta)))
        # make sure new is on the grid
        if new[0] >= 0 and new[0] < len(lst3) and new[1] >= 0 and new[1] < len(lst3[0]):
            height_new = lst3[new[0]][new[1]]
            # make sure we can walk to new
            if (height_new - height_current <= 1):
                # make sure we haven't already visited new
                if (new not in history):
                    history_copy.append(new)
                    print('Delta is', Delta, 'and history is now', history)
                    if new == E:
                        routes.append(history_copy.copy())
                        print('just added to routes! and the length is', len(routes[len(routes)-1]))
                        return
                    else:
                        print('in the else loop, just before calling the function recursively, history is', history)
                        walk(history_copy)





# walk([S])
# print('after calling the walk function, routes is', routes)

# # print(len(routes))
# # print(len(routes[0]))

# print('answer to part 1 is', min([len(route) for route in routes]) - 1)





### the above function is taking way too long! a speedup: run through all routes at the same rate, keeping track of them in a list, and discard a potential new route if _any_ old route has already reached its newest node.

routes_start = [[S]]

def lengthen_routes(routes):
    longer_routes = []
    for route in routes:
        current = route[len(route) - 1]
        height_current = lst3[current[0]][current[1]]
        Deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for Delta in Deltas:
            # make a copy of the route so we're not affecting the original version
            route_copy = route.copy()
            new = tuple(map(sum, zip(current, Delta)))
            # make sure new is on the grid
            if new[0] >= 0 and new[0] < len(lst3) and new[1] >= 0 and new[1] < len(lst3[0]):
                height_new = lst3[new[0]][new[1]]
                # make sure we can walk to new
                if (height_new - height_current <= 1):
                    # make sure we haven't already visited new, in _any_ of the previous routes
                    visited = False
                    for any_route in routes:
                        if new in any_route:
                            visited = True
                    if not visited:
                        route_copy.append(new)
                        longer_routes.append(route_copy)
    return longer_routes

def min_route():
    inner_routes = routes_start
    while True:
        print('there are', len(inner_routes), 'viable routes of length', len(inner_routes[0]))
        # print('now finding routes of length', len(inner_routes[0]) + 1)
        inner_routes = lengthen_routes(inner_routes)
        for route in inner_routes:
            if route[len(route)-1] == E:
                return len(route) - 1

print(min_route())