from CuckooHash import CuckooHash

import datetime

import re

course_sections = {
    'CS102: Data Structures and Algorithms': ['L1', 'L2', 'L3', 'L4', 'L5'],
    'CS102L: Data Structures and Algorithms Lab': ['T1', 'T2', 'T3', 'T4', 'T5'],
    'CS201: Data Structures 2': ['L1', 'L2', 'L3'],
    'CS224: Object Oriented Programming': ['L1', 'L2', 'L3'],
    'CS224L: Object Oriented Programming Lab': ['T1', 'T2', 'T3'],
    'CS101: Programming Fundamentals': ['L1'],
    'CS101L: Programming Fundamentals Lab': ['T1'],
    'CS375: Parallel Programming': ['L1'],
    'CS353: Software Engineering': ['L1', 'L2', 'L3'],
    'CS363: Networks, Games and Collective Behavior': ['L1'],
    'CS451: Computational Intelligence': ['L1'],
    'CS424: Joy of Theoretical Computer Science': ['L1']
}

course_times = {
    'CS102: Data Structures and Algorithms': ['Monday 8:30-11:00', 'Monday 13:30-16:00', 'Monday 8:30-11:00', 'Monday 13:30-16:00', 'Monday 13:30-16:00'],
    'CS102L: Data Structures and Algorithms Lab': ['Thursday 15:30-18:25', 'Thursday 15:30-18:25', 'Tuesday 15:30-18:25', 'Thursday 15:30-18:25', 'Wednesday 14:30-17:25'],
    'CS201: Data Structures 2': ['Tuesday 10:00-11:15\nThursday 10:00-11:15', 'Monday 15:50-17:05\nTuesday 12:00-13:15\nThursday 15:50-17:05', 'Wednesday 17:15-18:30\nFriday 17:15-18:30'],
    'CS224: Object Oriented Programming': ['Wednesday 8:30-11:00', 'Monday 16:00-18:30', 'Monday 10:30-13:00'],
    'CS224L: Object Oriented Programming Lab': ['Friday 8:30-11:25', 'Wednesday 15:30-18:25', 'Wednesday 10:30-13:25'],
    'CS101: Programming Fundamentals': ['Monday 12:30-13:20\nWednesday 12:30-13:20'],
    'CS101L: Programming Fundamentals Lab': ['Thursday 11:30-14:25'],
    'CS375: Parallel Programming': ['Monday 12:30-13:20\nThursday 15:30-17:10'],
    'CS353: Software Engineering': ['Tuesday 11:30-12:45\nThursday 11:30-12:45', 'Monday 11:30-12:45\nWednesday 11:30-12:45', 'Monday 13:00-14:15\nThursday 13:00-14:15'],
    'CS363: Networks, Games and Collective Behavior': ['Monday 14:25-15:40\nWednesday 14:25-15:40'],
    'CS451: Computational Intelligence': ['Tuesday 8:30-9:45\nThursday 8:30-9:45'],
    'CS424: Joy of Theoretical Computer Science': ['Wednesday 8:30-9:45\nFriday 8:30-9:45']
}

def data_extract(value, ch, my_lst):
    date = value[2].split('\n')
    for i in date:
        pair = (i, (value[0] + " " + value[1]))
    
        insertion = ch.insert(pair[0], pair[1])

        if insertion is not None:  # conflict 1st class
            my_lst.append((pair[0].split(" ")[0], insertion[0], insertion[1]))
            continue
        else:
            continue

def get_time(value):
    my_list = re.split(' |-', value)
    date_time_obj1 = datetime.datetime.strptime(my_list[1], '%H:%M')
    date_time_obj2 = datetime.datetime.strptime(my_list[2], '%H:%M')
    start_time = date_time_obj1.time()
    end_time = date_time_obj2.time()
    
    return my_list[0], start_time, end_time

def manual_conflict_check(keys, ch):
    conflicts = []

    for index, value in enumerate(keys):
        day, start_time, end_time = get_time(value)
        for j, data in enumerate(keys):
            if index == j: # avoid comparision against itself
                continue
            else:
                d, s_time, e_time = get_time(data)
                if e_time < start_time or s_time > end_time:
                    # print("no conflict", (index, j))
                    continue
                else:
                    if day == d:
                        if (day, ch.find(keys[j])[1], ch.find(keys[index])[1]) in conflicts:
                                continue
                        else:
                            conflicts.append((day, ch.find(keys[index])[1], ch.find(keys[j])[1])) # key[index]
                    else:
                        # print("no conflict", (index, j))
                        continue
    return conflicts

def check_conflict(data):
    direct_conflicts = []
    ch = CuckooHash(5)

    for i in data:
        data_extract(i, ch, direct_conflicts)

    table1, table2 = ch.Keys()

    table1_filtered = list(filter((None).__ne__, table1))
    table2_filtered = list(filter((None).__ne__, table2))

    intermediate_keys = table1_filtered + table2_filtered
    final_keys = [x[y] for x, y in zip(intermediate_keys, len(intermediate_keys)*[0])]

    indirect_conflicts = manual_conflict_check(final_keys, ch)

    all_conflicts = direct_conflicts + indirect_conflicts

    return all_conflicts