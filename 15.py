with open('15.txt') as file:
    str1 = file.read()


# example
example_str = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''


y0 = 2000000

# # un/comment this to toggle example vs actual data
# str1 = example_str
# y0 = 10


#########


lst1 = str1.split('\n')

def info_to_coords(strng):
    sensor_x = int(strng[strng.find("x=")+2:strng.find(",")])
    sensor_y = int(strng[strng.find("y=")+2:strng.find(":")])
    substrng = strng[strng.find(":"):]
    beacon_x = int(substrng[substrng.find("x=")+2:substrng.find(",")])
    beacon_y = int(substrng[substrng.find("y=")+2:])
    return ((sensor_x, sensor_y), (beacon_x, beacon_y))

lst = [info_to_coords(strng) for strng in lst1]

print('lst is', lst)

#########

### part 1

# we will end up with a finite union of (say N) closed intervals in the line y=y0. let's record such a thing as a list of 2-element tuples, recording the left and right endpoints of the intervals, in order from left to right.

# take the union of two intervals, assuming that they are ordered according to their left endpoints; return a list of intervals (also in order).
def union_two_intervals(int0, int1):
    if int0[1] < int1[0]:
        return [int0, int1]
    else:
        right = max(int0[1], int1[1])
        return [(int0[0], right)]

# take a list of not-necessarily-sorted and potentially overlapping intervals and reduce it to an ordered list of nonoverlapping intervals.
def reduce_intervals(intervals):
    intervals.sort(key = lambda tuple: tuple[0])
    i = 0
    while i < len(intervals) - 1:
        earlier = intervals[0:i]
        later = intervals[i+2:]
        new = union_two_intervals(intervals[i], intervals[i+1])
        intervals = earlier + new + later
        if len(new) == 2:
            i += 1
    return intervals

intervals_along_y0_line = []

def interval_along_y0_line(sensor, beacon):
    sensor_to_beacon = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    sensor_to_y0_line = abs(y0 - sensor[1])
    remainder = sensor_to_beacon - sensor_to_y0_line
    if remainder >= 0:
        left = sensor[0] - remainder
        right = sensor[0] + remainder
        return [(left, right)]
    else:
        return []
    
for pair in lst:
    intervals_along_y0_line = reduce_intervals(intervals_along_y0_line + interval_along_y0_line(pair[0], pair[1]))

print('the intervals along the y0 line are', intervals_along_y0_line)

beacons = set([pair[1] for pair in lst])

beacons_along_y0_line = {beacon for beacon in beacons if beacon[1] == y0}

answer_1 = 0

for interval in intervals_along_y0_line:
    answer_1 += interval[1] - interval[0] + 1

print('currently, answer_1 is', answer_1)

answer_1 -= len(beacons_along_y0_line)

print('answer to part 1 is', answer_1)


### part 2

# brute force (using the above): loop through y0 running from 0 to 4 million, and print any anomalies.



# for y0 in range(4000000):
first_y0_to_appear = 2638237

for y0 in range(4000000 - first_y0_to_appear + 5):
    y0 = y0 + 2638237 + 1
    print('y0 is', y0)
    intervals_along_y0_line = []
    for pair in lst:
        intervals_along_y0_line = reduce_intervals(intervals_along_y0_line + interval_along_y0_line(pair[0], pair[1]))
    if (len(intervals_along_y0_line) > 1) or (intervals_along_y0_line[0][0] > 0) or (intervals_along_y0_line[0][1] < 4000000):
        print('y0 is', y0, 'and intervals_along_y0_line is', intervals_along_y0_line)
        break

# output for range(4 million):
    # y0 is 2638237 and intervals_along_y0_line is [(-589410, 3270297), (3270299, 4077403)]
    # ... and no others!! (i only computed these because of a silly mistake in the other file, i set x=3270297 instead of 3270298.)
