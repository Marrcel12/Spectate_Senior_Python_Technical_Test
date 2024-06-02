def find_internal_nodes_num(L):
    """
    Calculate the number of internal nodes in a tree represented as a list.

    Args:
        L (List[int]): A list representing the tree structure. Each element in the list
            represents a node in the tree. The root node is represented by -1.

    Returns:
        int: The number of internal nodes in the tree.

    Example:
        >>> find_internal_nodes_num([-1, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
        5
    """
    return len(set((L)))-1