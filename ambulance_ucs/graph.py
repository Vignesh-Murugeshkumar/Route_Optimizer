import requests
import math

# Define nodes with real Chennai locations
NODES = {
    # ── HOSPITALS ──────────────────────────────────────────────
    "apollo": {
        "name": "Apollo Hospital, Greams Road",
        "lat": 13.0604, "lng": 80.2496,
        "type": "hospital"
    },
    "fortis": {
        "name": "Fortis Malar Hospital, Adyar",
        "lat": 13.0072, "lng": 80.2574,
        "type": "hospital"
    },
    "stanley": {
        "name": "Stanley Government Hospital, Royapuram",
        "lat": 13.1061, "lng": 80.2870,
        "type": "hospital"
    },
    "gggh": {
        "name": "Rajiv Gandhi Govt. General Hospital",
        "lat": 13.0827, "lng": 80.2707,
        "type": "hospital"
    },
    "vijaya": {
        "name": "Vijaya Hospital, Vadapalani",
        "lat": 13.0514, "lng": 80.2121,
        "type": "hospital"
    },

    # ── MAJOR INTERSECTIONS / LANDMARKS ────────────────────────
    "central": {
        "name": "Chennai Central Station",
        "lat": 13.0827, "lng": 80.2707,
        "type": "landmark"
    },
    "egmore": {
        "name": "Egmore Railway Station",
        "lat": 13.0732, "lng": 80.2609,
        "type": "landmark"
    },
    "tnagar": {
        "name": "T. Nagar Bus Terminus",
        "lat": 13.0418, "lng": 80.2341,
        "type": "landmark"
    },
    "adyar": {
        "name": "Adyar Signal Junction",
        "lat": 13.0012, "lng": 80.2565,
        "type": "landmark"
    },
    "anna_nagar": {
        "name": "Anna Nagar Tower Park",
        "lat": 13.0850, "lng": 80.2101,
        "type": "landmark"
    },
    "velachery": {
        "name": "Velachery Bus Terminus",
        "lat": 12.9815, "lng": 80.2180,
        "type": "landmark"
    },
    "mylapore": {
        "name": "Mylapore Tank Junction",
        "lat": 13.0368, "lng": 80.2676,
        "type": "landmark"
    },
    "tambaram": {
        "name": "Tambaram Railway Station",
        "lat": 12.9249, "lng": 80.1000,
        "type": "landmark"
    },
    "chromepet": {
        "name": "Chromepet Junction",
        "lat": 12.9516, "lng": 80.1462,
        "type": "landmark"
    },
    "guindy": {
        "name": "Guindy Metro Station",
        "lat": 13.0067, "lng": 80.2206,
        "type": "landmark"
    },
    "koyambedu": {
        "name": "Koyambedu Bus Stand",
        "lat": 13.0694, "lng": 80.1948,
        "type": "landmark"
    },
    "royapettah": {
        "name": "Royapettah Clock Tower",
        "lat": 13.0524, "lng": 80.2602,
        "type": "landmark"
    },
    "perambur": {
        "name": "Perambur Railway Station",
        "lat": 13.1143, "lng": 80.2485,
        "type": "landmark"
    },
    "madhavaram": {
        "name": "Madhavaram Milk Colony",
        "lat": 13.1490, "lng": 80.2337,
        "type": "landmark"
    },
    "sholinganallur": {
        "name": "Sholinganallur Junction",
        "lat": 12.9010, "lng": 80.2279,
        "type": "landmark"
    },
    "omr": {
        "name": "OMR Toll Plaza",
        "lat": 12.9345, "lng": 80.2298,
        "type": "landmark"
    },
    "porur": {
        "name": "Porur Junction",
        "lat": 13.0358, "lng": 80.1567,
        "type": "landmark"
    },
    "ambattur": {
        "name": "Ambattur Industrial Estate",
        "lat": 13.1143, "lng": 80.1548,
        "type": "landmark"
    },
    "avadi": {
        "name": "Avadi Bus Stand",
        "lat": 13.1152, "lng": 80.0980,
        "type": "landmark"
    },

    # ── EMERGENCY INCIDENT LOCATIONS ───────────────────────────
    "inc_besant": {
        "name": "Emergency — Besant Nagar Beach",
        "lat": 12.9990, "lng": 80.2707,
        "type": "incident"
    },
    "inc_marina": {
        "name": "Emergency — Marina Beach",
        "lat": 13.0500, "lng": 80.2824,
        "type": "incident"
    },
    "inc_vadapalani": {
        "name": "Emergency — Vadapalani Signal",
        "lat": 13.0525, "lng": 80.2121,
        "type": "incident"
    },
    "inc_chromepet": {
        "name": "Emergency — Chromepet Market",
        "lat": 12.9490, "lng": 80.1440,
        "type": "incident"
    },
    "inc_omr": {
        "name": "Emergency — OMR Perungudi",
        "lat": 12.9600, "lng": 80.2450,
        "type": "incident"
    },
    "inc_anna_nagar": {
        "name": "Emergency — Anna Nagar West",
        "lat": 13.0890, "lng": 80.2050,
        "type": "incident"
    },
    "inc_royapuram": {
        "name": "Emergency — Royapuram Fishing Harbour",
        "lat": 13.1100, "lng": 80.2990,
        "type": "incident"
    },
    "inc_tambaram": {
        "name": "Emergency — Tambaram East",
        "lat": 12.9230, "lng": 80.1150,
        "type": "incident"
    },
}

# Define edges as predefined list of connected nodes
# Format: (node_id_1, node_id_2)
# OSRM will auto-calculate real travel durations for each pair
EDGES = [
    # Central corridor
    ("central",       "egmore"),
    ("egmore",        "royapettah"),
    ("royapettah",    "mylapore"),
    ("mylapore",      "adyar"),
    ("adyar",         "fortis"),
    ("adyar",         "inc_besant"),

    # Marina / East coast
    ("central",       "inc_marina"),
    ("inc_marina",    "royapettah"),
    ("inc_marina",    "mylapore"),

    # North Chennai
    ("central",       "perambur"),
    ("perambur",      "stanley"),
    ("perambur",      "madhavaram"),
    ("stanley",       "inc_royapuram"),

    # West corridor
    ("egmore",        "tnagar"),
    ("tnagar",        "vijaya"),
    ("tnagar",        "inc_vadapalani"),
    ("tnagar",        "guindy"),
    ("guindy",        "velachery"),
    ("velachery",     "omr"),
    ("omr",           "sholinganallur"),
    ("sholinganallur","inc_omr"),

    # Apollo connections
    ("egmore",        "apollo"),
    ("royapettah",    "apollo"),
    ("apollo",        "mylapore"),

    # Anna Nagar / NW corridor
    ("anna_nagar",    "koyambedu"),
    ("anna_nagar",    "ambattur"),
    ("anna_nagar",    "inc_anna_nagar"),
    ("koyambedu",     "porur"),
    ("koyambedu",     "tnagar"),
    ("ambattur",      "avadi"),
    ("porur",         "guindy"),
    ("porur",         "vijaya"),
    ("vijaya",        "inc_vadapalani"),

    # South Chennai / OMR
    ("guindy",        "chromepet"),
    ("chromepet",     "tambaram"),
    ("chromepet",     "inc_chromepet"),
    ("tambaram",      "inc_tambaram"),
    ("velachery",     "sholinganallur"),
    ("omr",           "fortis"),

    # GGGH connections
    ("central",       "gggh"),
    ("egmore",        "gggh"),

    # Cross links
    ("mylapore",      "royapettah"),
    ("adyar",         "guindy"),
    ("anna_nagar",    "perambur"),
    ("avadi",         "madhavaram"),
    ("inc_anna_nagar","anna_nagar"),
    ("inc_chromepet", "chromepet"),
    ("inc_omr",       "omr"),
    ("inc_royapuram", "perambur"),
    ("inc_tambaram",  "tambaram"),
]

# In-memory cache for graph
_graph_cache = None


def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate distance between two coordinates using Haversine formula.
    Returns duration in seconds assuming 40 km/h average speed.
    """
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    distance_km = R * c
    
    # Assume 40 km/h average speed
    speed_kmh = 40
    duration_hours = distance_km / speed_kmh
    duration_seconds = duration_hours * 3600
    
    return duration_seconds


def fetch_osrm_durations(node_pairs):
    """
    Fetch travel durations from OSRM table API.
    
    Args:
        node_pairs: list of tuples (node_id1, node_id2)
    
    Returns:
        dict mapping (node_id1, node_id2) -> duration_seconds
        Falls back to Haversine if OSRM is unavailable
    """
    result = {}
    
    try:
        # Get unique nodes from pairs
        unique_nodes = set()
        for n1, n2 in node_pairs:
            unique_nodes.add(n1)
            unique_nodes.add(n2)
        
        unique_nodes = sorted(list(unique_nodes))
        
        # Build coordinates string for OSRM
        coords = ";".join([f"{NODES[n]['lng']},{NODES[n]['lat']}" for n in unique_nodes])
        
        # Call OSRM table API
        url = f"https://router.project-osrm.org/table/v1/driving/{coords}?sources=all&destinations=all&annotations=duration"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") != "Ok":
            raise Exception(f"OSRM error: {data.get('message')}")
        
        durations = data.get("durations", [])
        
        # Map results back to node pairs
        for n1, n2 in node_pairs:
            idx1 = unique_nodes.index(n1)
            idx2 = unique_nodes.index(n2)
            duration = durations[idx1][idx2]
            result[(n1, n2)] = duration
        
        return result
    
    except Exception as e:
        print(f"OSRM fetch failed: {e}. Using Haversine fallback.")
        # Fall back to Haversine
        for n1, n2 in node_pairs:
            if n1 in NODES and n2 in NODES:
                duration = haversine(
                    NODES[n1]["lat"], NODES[n1]["lng"],
                    NODES[n2]["lat"], NODES[n2]["lng"]
                )
                result[(n1, n2)] = duration
        return result


def get_route_geometry(start_node_id, end_node_id):
    """
    Get polyline coordinates from OSRM route API.
    
    Args:
        start_node_id: starting node identifier
        end_node_id: ending node identifier
    
    Returns:
        list of [lat, lng] coordinates for the route
        Falls back to straight line if OSRM fails
    """
    try:
        start = NODES[start_node_id]
        end = NODES[end_node_id]
        
        url = f"https://router.project-osrm.org/route/v1/driving/{start['lng']},{start['lat']};{end['lng']},{end['lat']}?overview=full&geometries=geojson"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("code") != "Ok" or not data.get("routes"):
            raise Exception("No route found")
        
        route = data["routes"][0]
        geometry = route.get("geometry", {})
        coordinates = geometry.get("coordinates", [])
        
        # Convert from [lng, lat] to [lat, lng]
        return [[lat, lng] for lng, lat in coordinates]
    
    except Exception as e:
        print(f"OSRM route fetch failed: {e}. Using straight line.")
        # Fall back to straight line
        start = NODES[start_node_id]
        end = NODES[end_node_id]
        return [
            [start["lat"], start["lng"]],
            [end["lat"], end["lng"]]
        ]


def build_graph(nodes=None, edges=None):
    """
    Build adjacency list graph from nodes and edges using OSRM data.
    
    Returns:
        dict: {node_id: [(neighbor_id, duration_seconds), ...]}
    """
    global _graph_cache
    
    if _graph_cache is not None:
        return _graph_cache
    
    if nodes is None:
        nodes = NODES
    if edges is None:
        edges = EDGES
    
    # Fetch durations for all edges
    durations = fetch_osrm_durations(edges)
    
    # Build adjacency list
    graph = {}
    for node_id in nodes:
        graph[node_id] = []
    
    # Add edges (bidirectional)
    for n1, n2 in edges:
        duration = durations.get((n1, n2), 0)
        graph[n1].append((n2, duration))
        graph[n2].append((n1, duration))
    
    _graph_cache = graph
    return graph


def refresh_graph():
    """Force refresh of graph cache."""
    global _graph_cache
    _graph_cache = None
    return build_graph()
