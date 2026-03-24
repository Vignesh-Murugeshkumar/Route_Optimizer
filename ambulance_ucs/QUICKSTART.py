#!/usr/bin/env python
"""
QUICK START GUIDE - Ambulance Route Optimization System
========================================================

This script documents how to run the system.
Execute: python app.py
"""

import sys
import os

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║        AMBULANCE ROUTE OPTIMIZATION SYSTEM                    ║
    ║        Uniform Cost Search with Real Road Data                ║
    ║                                                                ║
    ║        Status: ✅ FULLY IMPLEMENTED & OPERATIONAL             ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_structure():
    print("\n📁 PROJECT STRUCTURE:\n")
    structure = """
    ambulance_ucs/
    ├── app.py                 ⚙️  Flask API server
    ├── ucs.py                 🔍 UCS algorithm (heapq)
    ├── graph.py               🗺️  Graph builder + OSRM
    ├── requirements.txt        📦 Dependencies
    ├── test_system.py          ✅ System tests (5/5 passing)
    ├── README.md               📖 Full documentation
    ├── templates/
    │   └── index.html          🌐 Leaflet map interface
    └── static/
        ├── map.js              🎨 Frontend logic
        └── style.css           💄 Styling
    """
    print(structure)

def print_quick_start():
    print("\n⚡ QUICK START:\n")
    start = """
    Step 1: Navigate to project directory
    $ cd d:\\PROJECTS\\ambulance\\ambulance_ucs

    Step 2: (Optional) Install dependencies
    $ pip install -r requirements.txt

    Step 3: Start the Flask server
    $ python app.py

    Step 4: Open browser
    → http://localhost:5000

    Step 5: Use the application
    • Select Emergency Location (incident)
    • Select Destination Hospital
    • Click "Run UCS"
    • Watch algorithm explore the map!
    """
    print(start)

def print_features():
    print("\n✨ FEATURES:\n")
    features = """
    ✓ Real UCS Algorithm         Using Python heapq priority queue
    ✓ Real Road Data             Via OSRM public API (free)
    ✓ Interactive Map            Leaflet.js with 12 Chennai locations
    ✓ Animation                  350ms per frontier expansion
    ✓ Live Stats                 Route, time, explored nodes
    ✓ Error Handling             Haversine fallback if OSRM down
    ✓ Responsive UI              Split-screen (40% controls, 60% map)
    ✓ Comprehensive Tests        5/5 tests passing ✅
    """
    print(features)

def print_api_endpoints():
    print("\n🔌 API ENDPOINTS:\n")
    endpoints = """
    GET  http://localhost:5000/
         → Serve main HTML page

    GET  http://localhost:5000/api/nodes
         → Return all 12 locations with coordinates

    GET  http://localhost:5000/api/graph
         → Build and return graph with edges + OSRM durations

    POST http://localhost:5000/api/solve
         → Run UCS algorithm
         Body: {"start": "incident_1", "goal": "apollo"}

    GET  http://localhost:5000/api/graph/refresh
         → Force re-fetch from OSRM
    """
    print(endpoints)

def print_testing():
    print("\n🧪 TESTING:\n")
    testing = """
    Run the comprehensive test suite:
    $ python test_system.py

    Tests included:
    ✓ API nodes endpoint
    ✓ Graph building with OSRM
    ✓ UCS algorithm execution
    ✓ Error handling (invalid nodes)
    ✓ Graph refresh endpoint

    Expected: 5/5 tests passing ✅
    """
    print(testing)

def print_navigation():
    print("\n🗺️  NAVIGATION:\n")
    nav = """
    Left Panel (40%):
    • Dropdowns for incident/hospital selection
    • Run UCS, Reset, Random Emergency buttons
    • Route statistics
    • Priority queue live view
    • Expansion history log

    Right Panel (60%):
    • Interactive Leaflet map of Chennai
    • Markers for all locations
    • Gray edges showing road network
    • Green markers = explored nodes
    • Orange markers & path = optimal route
    """
    print(nav)

def print_example():
    print("\n📍 EXAMPLE SCENARIO:\n")
    example = """
    Accident in Adyar → Need to reach Apollo Hospital

    1. User selects:
       • Start: "Emergency - Adyar"
       • Goal: "Apollo Hospital"

    2. Backend runs UCS:
       • Explores nodes by cost
       • Finds optimal path: incident_1 → mylapore → apollo
       • Total time: 14.8 minutes

    3. Frontend animates:
       • Each node expands at 350ms intervals (green ✓)
       • Draws optimal path in orange
       • Shows stats: route, time, nodes explored
       • Displays expansion log
    """
    print(example)

def print_troubleshooting():
    print("\n🔧 TROUBLESHOOTING:\n")
    troubleshoot = """
    Problem: "OSRM requests failing"
    Solution: System uses Haversine fallback. Check internet.

    Problem: "Port 5000 already in use"
    Solution: Kill existing process or change port in app.py

    Problem: "Flask module not found"
    Solution: pip install -r requirements.txt

    Problem: "Graph not loading on map"
    Solution: Check browser console. Ensure Flask running.

    Problem: "Dropdown empty"
    Solution: Wait for /api/graph to complete (spinner).
    """
    print(troubleshoot)

def print_tech_stack():
    print("\n⚙️  TECHNOLOGY STACK:\n")
    tech = """
    Backend:
    • Python 3.13
    • Flask 3.0.0 (web framework)
    • Flask-CORS 4.0.0 (cross-origin requests)
    • Requests 2.31.0 (HTTP client)

    Algorithm:
    • Uniform Cost Search (UCS)
    • heapq module (priority queue)
    • Haversine formula (fallback distance)

    Frontend:
    • HTML5
    • Leaflet.js (interactive maps)
    • OpenStreetMap tiles (map data)
    • Vanilla JavaScript (no frameworks)
    • Pure CSS3 (no preprocessors)

    APIs:
    • OSRM (Open Source Routing Machine)
      - Table API: travel durations
      - Route API: polyline coordinates
    """
    print(tech)

def main():
    print_banner()
    print_structure()
    print_quick_start()
    print_features()
    print_api_endpoints()
    print_testing()
    print_navigation()
    print_example()
    print_troubleshooting()
    print_tech_stack()
    
    print("\n" + "="*65)
    print("🚀 Ready to start? Run: python app.py")
    print("🌐 Then open: http://localhost:5000")
    print("="*65 + "\n")

if __name__ == "__main__":
    main()
