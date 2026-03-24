"""
Comprehensive system tests for Ambulance Route Optimization
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_nodes_api():
    """Test: Fetch all nodes from backend"""
    print("TEST 1: GET /api/nodes")
    try:
        resp = requests.get(f"{BASE_URL}/api/nodes")
        nodes = resp.json()
        assert len(nodes) == 32, f"Expected 32 nodes, got {len(nodes)}"
        print(f"  ✓ Loaded {len(nodes)} nodes")
        print(f"    Sample: {list(nodes.keys())[:3]}")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

def test_graph_api():
    """Test: Build graph with OSRM data"""
    print("\nTEST 2: GET /api/graph")
    try:
        resp = requests.get(f"{BASE_URL}/api/graph")
        data = resp.json()
        assert data["success"], "Graph build failed"
        assert len(data["graph"]) == 32, f"Graph has {len(data['graph'])} nodes, expected 32"
        assert len(data["edges"]) == 50, f"Graph has {len(data['edges'])} edges, expected 50"
        print(f"  ✓ Graph built successfully")
        print(f"    Nodes: {len(data['graph'])}, Edges: {len(data['edges'])}")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

def test_ucs_algorithm():
    """Test: Run UCS algorithm end-to-end"""
    print("\nTEST 3: POST /api/solve (UCS Algorithm)")
    try:
        payload = {"start": "inc_marina", "goal": "apollo"}
        resp = requests.post(f"{BASE_URL}/api/solve", json=payload)
        result = resp.json()
        
        assert result["found"], "No path found"
        assert len(result["path"]) > 1, "Invalid path"
        assert result["total_cost_minutes"] > 0, "Invalid cost"
        assert len(result["explored_order"]) > 0, "No exploration log"
        assert len(result["route_geometry"]) > 0, "No route geometry"
        
        print(f"  ✓ UCS algorithm executed successfully")
        print(f"    Path: {' → '.join(result['path'])}")
        print(f"    Travel time: {result['total_cost_minutes']:.1f} minutes")
        print(f"    Nodes explored: {len(result['explored_order'])}")
        print(f"    Route segments: {len(result['route_geometry'])}")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

def test_invalid_nodes():
    """Test: Error handling for invalid nodes"""
    print("\nTEST 4: GET /api/solve with invalid nodes")
    try:
        payload = {"start": "invalid_1", "goal": "invalid_2"}
        resp = requests.post(f"{BASE_URL}/api/solve", json=payload)
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
        print(f"  ✓ Invalid nodes rejected correctly (HTTP 400)")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

def test_graph_refresh():
    """Test: Graph refresh endpoint"""
    print("\nTEST 5: GET /api/graph/refresh")
    try:
        resp = requests.get(f"{BASE_URL}/api/graph/refresh")
        data = resp.json()
        assert data["success"], "Graph refresh failed"
        print(f"  ✓ Graph refresh successful")
        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

def main():
    print("="*50)
    print("AMBULANCE ROUTE OPTIMIZATION SYSTEM - TEST SUITE")
    print("="*50)
    
    tests = [
        test_nodes_api,
        test_graph_api,
        test_ucs_algorithm,
        test_invalid_nodes,
        test_graph_refresh
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "="*50)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("="*50)
    
    if all(results):
        print("\n✅ ALL TESTS PASSED - System is fully operational!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
