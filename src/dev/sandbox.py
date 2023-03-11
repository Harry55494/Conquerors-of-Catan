import time

player_1_roads = [
    ["A", "B"],
    ["B", "C"],
    ["C", "D"],
    ["B", "E"],
    ["E", "F"],
    ["F", "G"],
    ["F", "H"],
]


def find_longest_route(paths):
    # create a dictionary to store the adjacency list of the graph
    adj_list = {}
    for path in paths:
        a, b = path
        if a not in adj_list:
            adj_list[a] = set()
        if b not in adj_list:
            adj_list[b] = set()
        adj_list[a].add(b)
        adj_list[b].add(a)

    # initialize variables for tracking the longest route and current path
    longest_route = []
    current_path = []

    # recursively find the longest route starting from the first node
    find_route_from_node(
        list(adj_list.keys())[0], adj_list, set(), set(), longest_route, current_path
    )

    return longest_route


def find_route_from_node(
    node, adj_list, visited, used_paths, longest_route, current_path
):
    visited.add(node)
    current_path.append(node)

    # check if the current path is longer than the longest route so far
    if len(current_path) > len(longest_route):
        longest_route[:] = current_path

    # recursively explore all unexplored neighbors of the node
    unexplored_neighbors = [
        neighbor for neighbor in adj_list[node] if neighbor not in visited
    ]
    if len(unexplored_neighbors) == 1:
        # if there is only one unexplored neighbor, continue exploring that path
        find_route_from_node(
            unexplored_neighbors[0],
            adj_list,
            visited,
            used_paths,
            longest_route,
            current_path,
        )
    elif len(unexplored_neighbors) > 1:
        # if there are multiple unexplored neighbors, mark this as a fork in the road
        for neighbor in unexplored_neighbors:
            path = frozenset([node, neighbor])
            if path not in used_paths:
                used_paths.add(path)
                find_route_from_node(
                    neighbor,
                    adj_list,
                    visited.copy(),
                    used_paths.copy(),
                    longest_route,
                    current_path.copy(),
                )
                used_paths.remove(path)

    # remove the current node from the visited set and current path
    visited.remove(node)
    current_path.pop()


start = time.time()


longest = find_longest_route(player_1_roads)
print(longest)
print(len(longest) - 1)

end = time.time()
# format time taken to 2 decimal places
print(f"Time taken: {end - start:.20f}s")
