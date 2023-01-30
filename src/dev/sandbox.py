roads_1 = [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"], ["e", "f"], ["f", "g"]]
roads_2 = [
    ["a", "b"],
    ["b", "c"],
    ["d", "e"],
    ["e", "f"],
    ["f", "g"],
    ["g", "h"],
    ["i", "j"],
]


def get_road_length():
    def return_clusers(set):
        # cluster roads based on their connections
        clusters = []
        for road in set:
            for cluster in clusters:
                for node in cluster:
                    if road[0] in node or road[1] in node:
                        # print("N", node, "R", road)
                        cluster.extend([road])
                        break
            else:
                if road not in [item for sublist in clusters for item in sublist]:
                    clusters.append([road])

        # pair up roads that are connected to each other

        return clusters

    for set in [roads_1, roads_2]:
        print("S", set)
        for cluster in return_clusers(set):
            print("C", cluster)

        print(max([len(cluster) for cluster in return_clusers(set)]))


if __name__ == "__main__":
    get_road_length()
