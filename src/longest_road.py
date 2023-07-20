"""
Methods to find the longest route in a graph.
ChatGPT wrote some code as listed below

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com. For the full licence, please see LICENCE.txt (https://github.com/Harry55494/conquerors-of-catan/blob/master/LICENCE)
"""


# Using AI to write an AI program is ironic haha

# CHATGPT HAS WRITTEN THIS CODE ------------------------------------------------


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

    # recursively explore all unexplored neighbours of the node
    unexplored_neighbours = [
        neighbour for neighbour in adj_list[node] if neighbour not in visited
    ]
    if len(unexplored_neighbours) == 1:
        # if there is only one unexplored neighbour, continue exploring that path
        find_route_from_node(
            unexplored_neighbours[0],
            adj_list,
            visited,
            used_paths,
            longest_route,
            current_path,
        )
    elif len(unexplored_neighbours) > 1:
        # if there are multiple unexplored neighbours, mark this as a fork in the road
        for neighbour in unexplored_neighbours:
            path = frozenset([node, neighbour])
            if path not in used_paths:
                used_paths.add(path)
                find_route_from_node(
                    neighbour,
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


# END OF CHATGPT'S CODE -------------------------------------------------------


# Method to find the clusters of roads that are together
def return_clusters(set):
    clusters = []
    # Iterates through every road that the player owns
    for road in set:
        # Checks through all existing clusters
        for cluster in clusters:
            # For every road in the cluster, check if the current road is connected to it
            for node in cluster:
                if road[0] in node or road[1] in node:
                    # If it is, add the current road to the cluster, otherwise do nothing
                    cluster.extend([road])
                    break
        else:
            # If the road is not connected to any other road create a new cluster
            if road not in [item for sublist in clusters for item in sublist]:
                clusters.append([road])

    return clusters
