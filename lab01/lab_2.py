import copy
import pprint
from gps import gps


def op_generator():
    objects = ["a", "b", "c"]
    objects_copy = ["a", "b", "c"]
    positions = ["1", "2", "3"]
    positions_copy = copy.deepcopy(positions)

    ops = []

    for object in objects:
        # choose a letter and remove it from the set
        objects_copy.remove(object)

        for position in positions:
            positions_copy.remove(position)

            # to avoid moving to the same position, we use a list that has the current position removed
            for original_position in positions_copy:
                # from table to table
                ops.append({
                    "action": "move " + object + " from " + original_position + " to " + position,
                    "preconds": [
                        "space on " + position,
                        "space on " + object,
                        object + " at " + original_position
                    ],
                    "add": [
                        object + " at " + position,
                        "space on " + original_position,
                    ],
                    "delete": [
                        "space on " + position,
                        object + " at " + original_position
                    ]
                })

                for base_object in objects_copy:
                    # from other box to table
                    ops.append({
                        "action": "move " + object + " from " + base_object + " at " + original_position + " to " +
                                  position,
                        "preconds": [
                            "space on " + position,
                            "space on " + object,
                            object + " on " + base_object,
                            base_object + " at " + original_position,
                        ],
                        "add": [
                            "space on " + base_object,
                            object + " at " + position,
                        ],
                        "delete": [
                            "space on " + position,
                            object + " on " + base_object,
                        ]
                    })
                    # from table to box
                    ops.append({
                        "action": "move " + object + " from " + original_position + " to " + base_object + " at " +
                                  position,
                        "preconds": [
                            "space on " + base_object,
                            "space on " + object,
                            object + " at " + original_position,
                            base_object + " at " + position,
                        ],
                        "add": [
                            "space on " + original_position,
                            object + " at " + position,
                            object + " on " + base_object,
                        ],
                        "delete": [
                            "space on " + base_object,
                            object + " at " + original_position,
                        ]
                    })

                    # form box to box
                    temp_obj = copy.deepcopy(objects_copy)
                    temp_obj.remove(base_object)

                    for destination in temp_obj:
                        ops.append({
                            "action": "move " + object + " from " + base_object + " at " + original_position + " to " +
                                      destination + " at " + position,
                            "preconds": [
                                "space on " + object,
                                object + " on " + base_object,
                                base_object + " at " + original_position,
                                "space on " + destination,
                                destination + " at " + position,
                            ],
                            "add": [
                                "space on " + base_object,
                                object + " at " + position,
                            ],
                            "delete": [
                                "space on " + destination,
                                object + " on " + base_object,
                            ]
                        })

            positions_copy = copy.deepcopy(positions)

        objects_copy = copy.deepcopy(objects)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(ops)
    print("length: ", len(ops))

    return ops


problem = {
    "start1": ["space on a", "a on b", "b on c", "c on table", "space on table"],
    "finish1": ["space on c", "c on b", "b on a", "a on table", "space on table"],

    "start2": ["space on 1", "space on b", "b at 2", "c on a", "a at 1", "c at 1"],
    "finish2": ["b at 1", "a at 2", "c at 3", "space on b", "space on a", "space on c"],

    "start3": ["space on b", "b on table", "space on a", "a on table", "space on c", "c on table"],
    "finish3": ["space on a", "s on b", "b on c", "c on table", "space on table"],

    # settings for the Sussman Anamoly, see PAIP, pp. 142.
    "sussmanStart": ["space on c", "c on a", "a on table", "b on table", "space on table"],
    "sussmanFinish": ["space on a", "a on b", "b on c", "c on table", "space on table"],

    "ops": [
        {
            "action": "move a from b to c",
            "preconds": [
                "space on a",
                "space on c",
                "a on b"
            ],
            "add": [
                "a on c",
                "space on b"
            ],
            "delete": [
                "a on b",
                "space on c"
            ]
        },
        {
            "action": "move a from table to b",
            "preconds": [
                "space on a",
                "space on b",
                "a on table"
            ],
            "add": [
                "a on b"
            ],
            "delete": [
                "a on table",
                "space on b"
            ]
        },
        {
            "action": "move a from b to table",
            "preconds": [
                "space on a",
                "space on table",
                "a on b"
            ],
            "add": [
                "a on table",
                "space on b"
            ],
            "delete": [
                "a on b"
            ]
        },
        {
            "action": "move a from c to b",
            "preconds": [
                "space on a",
                "space on b",
                "a on c"
            ],
            "add": [
                "a on b",
                "space on c"
            ],
            "delete": [
                "a on c",
                "space on b"
            ]
        },
        {
            "action": "move a from table to c",
            "preconds": [
                "space on a",
                "space on c",
                "a on table"
            ],
            "add": [
                "a on c"
            ],
            "delete": [
                "a on table",
                "space on c"
            ]
        },
        {
            "action": "move a from c to table",
            "preconds": [
                "space on a",
                "space on table",
                "a on c"
            ],
            "add": [
                "a on table",
                "space on c"
            ],
            "delete": [
                "a on c"
            ]
        },
        {
            "action": "move b from a to c",
            "preconds": [
                "space on b",
                "space on c",
                "b on a"
            ],
            "add": [
                "b on c",
                "space on a"
            ],
            "delete": [
                "b on a",
                "space on c"
            ]
        },
        {
            "action": "move b from table to a",
            "preconds": [
                "space on b",
                "space on a",
                "b on table"
            ],
            "add": [
                "b on a"
            ],
            "delete": [
                "b on table",
                "space on a"
            ]
        },
        {
            "action": "move b from a to table",
            "preconds": [
                "space on b",
                "space on table",
                "b on a"
            ],
            "add": [
                "b on table",
                "space on a"
            ],
            "delete": [
                "b on a"
            ]
        },
        {
            "action": "move b from c to a",
            "preconds": [
                "space on b",
                "space on a",
                "b on c"
            ],
            "add": [
                "b on a",
                "space on c"
            ],
            "delete": [
                "b on c",
                "space on a"
            ]
        },
        {
            "action": "move b from table to c",
            "preconds": [
                "space on b",
                "space on c",
                "b on table"
            ],
            "add": [
                "b on c"
            ],
            "delete": [
                "b on table",
                "space on c"
            ]
        },
        {
            "action": "move b from c to table",
            "preconds": [
                "space on b",
                "space on table",
                "b on c"
            ],
            "add": [
                "b on table",
                "space on c"
            ],
            "delete": [
                "b on c"
            ]
        },
        {
            "action": "move c from a to b",
            "preconds": [
                "space on c",
                "space on b",
                "c on a"
            ],
            "add": [
                "c on b",
                "space on a"
            ],
            "delete": [
                "c on a",
                "space on b"
            ]
        },
        {
            "action": "move c from table to a",
            "preconds": [
                "space on c",
                "space on a",
                "c on table"
            ],
            "add": [
                "c on a"
            ],
            "delete": [
                "c on table",
                "space on a"
            ]
        },
        {
            "action": "move c from a to table",
            "preconds": [
                "space on c",
                "space on table",
                "c on a"
            ],
            "add": [
                "c on table",
                "space on a"
            ],
            "delete": [
                "c on a"
            ]
        },
        {
            "action": "move c from b to a",
            "preconds": [
                "space on c",
                "space on a",
                "c on b"
            ],
            "add": [
                "c on a",
                "space on b"
            ],
            "delete": [
                "c on b",
                "space on a"
            ]
        },
        {
            "action": "move c from table to b",
            "preconds": [
                "space on c",
                "space on b",
                "c on table"
            ],
            "add": [
                "c on b"
            ],
            "delete": [
                "c on table",
                "space on b"
            ]
        },
        {
            "action": "move c from b to table",
            "preconds": [
                "space on c",
                "space on table",
                "c on b"
            ],
            "add": [
                "c on table",
                "space on b"
            ],
            "delete": [
                "c on b"
            ]
        }
    ],

    "opsMod": op_generator()
}


#
def main():
    start1 = problem['start1']
    finish1 = problem['finish1']

    start2 = problem['start2']
    finish2 = problem['finish2']

    start3 = problem['start3']
    finish3 = problem['finish3']

    ops = problem['ops']
    ops_mod = problem['opsMod']

    action_sequences1 = gps(start1, finish1, ops)
    action_sequences2 = gps(start2, finish2, ops_mod)
    action_sequences3 = gps(start3, finish3, ops)

    labels = [
        "default----------------------\n",
        "\nExercise 1.2.a --------------\n",
        "\nExercise 1.2.b --------------\n",
    ]

    print(labels[0])
    if action_sequences1 is None:
        print("plan failure...")
    else:
        for action in action_sequences1:
            print(action)

    print(labels[1])
    if action_sequences2 is None:
        print("plan failure...")
    else:
        for action in action_sequences2:
            print(action)

    print(labels[2])
    if action_sequences3 is None:
        print("plan failure...")
    else:
        for action in action_sequences3:
            print(action)


if __name__ == '__main__':
    main()
