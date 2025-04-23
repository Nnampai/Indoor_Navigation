import config

# Define variable from config
graph = config.GRAPH
distances = config.DISTANCES
coordinated = config.COORDINATES

last_node_idx = 0
visited_node = {}

def euclidean(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5  # sqrt for real distance

def heuristic(start, goal):  # location_name
    global coordinated
    return euclidean(coordinated[start][0], coordinated[start][1],
                     coordinated[goal][0], coordinated[goal][1])

def gen_successors(node, goal_loc):
    global graph
    global distances
    global last_node_idx
    location_name, node_id, parent_id, cost, f = node
    childs = []  # list of child nodes
    for child in graph.get(location_name, []):  # Check if location_name exists in graph
        # Check key and reverse key
        if (location_name, child) in distances:
            dist = distances[(location_name, child)]
        elif (child, location_name) in distances:
            dist = distances[(child, location_name)]
        else: # if no key, skip this node
            continue

        last_node_idx += 1  # Increase node ID counter
        g_cost = cost + dist  # cost/g
        f_cost = g_cost + heuristic(child, goal_loc)  # f = g + h
        childs.append((child, last_node_idx, node_id, g_cost, f_cost))
    return childs

def insert_all(node, fringe, goal_loc):
    children = gen_successors(node, goal_loc)
    for child in children:
        inserted = False
        for j in range(len(fringe)):
            if child[4] < fringe[j][4]:  # Sort by f-cost
                fringe.insert(j, child)
                inserted = True
                break
        if not inserted:
            fringe.append(child)

def show_result(current_node, visited_node):
    path = []
    while current_node[2] != -1:  # Backtrack using parent_id
        path.append(current_node[0])
        current_node = visited_node[current_node[2]]
    path.append(current_node[0])  # Add start node
    return path[::-1]  # Reverse path to get start → goal

def a_star(start_loc,goal_loc):
    global last_node_idx
    global visited_node

    start_node = (start_loc, 0, -1, 0, 0)  # node
    # node = (location_name, node_id, parent_id, cost, f)
    # node_id: Identify each node
    # parent_id: Use the reverse route
    # cost/g(n): Distance of start node to current node
    # f: f(n) = g(n) + h(n)/heuristic

    last_node_idx = 0
    fringe = [start_node]
    visited_node = {}

    while fringe:
        front = fringe.pop(0)  # Get node with lowest f-cost
        visited_node[front[1]] = front  # Store in visited

        if front[0] == goal_loc:
            path = show_result(front, visited_node)
            # print("Path found:", path)
            total_dist = front[3]
            return path, total_dist

        insert_all(front, fringe, goal_loc)

    print("No path found")
    return []