import heapq

def uniform_cost_search(graph, start, goal):
    """
    Uniform Cost Search implementation using heapq.
    
    Args:
        graph: dict of {node_id: [(neighbor_id, cost), ...]}
        start: starting node_id
        goal: goal node_id
    
    Returns:
        dict with:
        - path: list of node ids from start to goal
        - total_cost_seconds: float (total time in seconds)
        - total_cost_minutes: float (total time in minutes)
        - explored_order: list of dicts with {node, cumulative_cost, path_so_far}
        - found: bool (True if goal was reached)
    """
    frontier = []
    heapq.heappush(frontier, (0, start, [start]))
    explored = set()
    explored_order = []

    while frontier:
        cost, node, path = heapq.heappop(frontier)
        
        # Skip if already explored
        if node in explored:
            continue
        
        explored.add(node)
        explored_order.append({
            "node": node,
            "cumulative_cost": round(cost / 60, 2),
            "path_so_far": path[:]
        })
        
        # Check if goal reached
        if node == goal:
            return {
                "path": path,
                "total_cost_seconds": cost,
                "total_cost_minutes": round(cost / 60, 2),
                "explored_order": explored_order,
                "found": True
            }
        
        # Add neighbors to frontier
        for neighbor, weight in graph.get(node, []):
            if neighbor not in explored:
                heapq.heappush(frontier, 
                    (cost + weight, neighbor, path + [neighbor]))

    return {
        "path": [],
        "total_cost_seconds": 0,
        "total_cost_minutes": 0,
        "explored_order": explored_order,
        "found": False
    }
