from tree import find_internal_nodes_num


def test_find_internal_nodes_num():
    test_cases = [
        ([-1], 0),  # Single node (root), no internal nodes
        ([-1, 0], 1),  # Root with one child
        ([-1, 0, 0], 1),  # Root with two children
        ([-1, 0, 0, 1], 2),  # Root with two children, one child has its own child
        ([-1, 0, 1, 1, 1], 2),  # Root with one child, that child has three children
        ([-1, 0, 0, 0, 0, 0, 0], 1),  # Root with six children
        ([-1, 0, 1, 1, 2, 2, 3, 3], 4),  # Complex tree structure
        (
            [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4],
            5,
        ),  # Complex tree structure with deeper levels
        ([-1, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4], 5),  # Multiple internal nodes
        (
            [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            10,
        ),  # Each node has one child, forming a linear structure
        (
            [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9],
            10,
        ),  # Complex with multiple branches
        (
            [-1, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6],
            7,
        ),  # Even distribution of children
        (
            [-1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            2,
        ),  # Single deep branch
        (
            [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            19,
        ),  # Linear deep branch
        (
            [-1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3],
            4,
        ),  # Broad tree with some internal nodes having many children
        (
            [-1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
            7,
        ),  # Combination of broad and deep structure
        (
            [-1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4],
            5,
        ),  # Complex structure
        (
            [
                -1,
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
            ],
            26,
        ),  # Long linear structure
        (
            [
                -1,
                0,
                1,
                1,
                1,
                2,
                2,
                2,
                3,
                3,
                3,
                4,
                4,
                4,
                5,
                5,
                5,
                6,
                6,
                6,
                7,
                7,
                7,
                8,
                8,
                8,
                9,
            ],
            10,
        ),  # Broad tree with many children
        (
            [
                -1,
                0,
                0,
                1,
                1,
                1,
                2,
                2,
                2,
                3,
                3,
                3,
                4,
                4,
                4,
                5,
                5,
                5,
                6,
                6,
                6,
                7,
                7,
                7,
                8,
                8,
                8,
                9,
                9,
                9,
            ],
            10,
        ),  # Very broad tree with repeated internal nodes
        ([4, 4, 1, 5, -1, 4, 5], 3),  # example from the problem statement
    ]

    for i, (L, expected) in enumerate(test_cases):
        result = find_internal_nodes_num(L)
        assert (
            result == expected
        ), f"Test case {i+1} failed for new: expected {expected}, got {result}"
        print(f"Test case {i+1} passed: {result} == {expected}")
