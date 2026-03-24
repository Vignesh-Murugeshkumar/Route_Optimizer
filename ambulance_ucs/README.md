# Ambulance Route Optimization System

## Overview

A full-stack ambulance routing system that uses the **Uniform Cost Search (UCS)** algorithm to find optimal routes between emergency locations and hospitals in Chennai. The system integrates real road network data from OSRM (Open Source Routing Machine) and visualizes the algorithm's exploration process on an interactive Leaflet.js map.

### Key Features

- ⚡ **Real-time Route Optimization** using UCS algorithm (priority queue-based)
- 🗺️ **Interactive Map Visualization** with Leaflet.js and OpenStreetMap tiles
- 🛣️ **Real Road Data** via OSRM Public API (no authentication required)
- 📊 **Live Algorithm Animation** - Watch each node expansion at 350ms intervals
- 🏥 **12 Real Chennai Locations** - 3 hospitals, 7 landmarks, 2 emergency points
- 🔀 **20 Relief Edges** - Predefined realistic road network topology
- 📱 **Responsive Split-Screen UI** - 40% controls + 60% map
- 💾 **In-Memory Graph Cache** - OSRM data cached for performance
- 🛡️ **Fallback Handling** - Haversine distance fallback if OSRM unavailable
- ✅ **Comprehensive Error Handling** - Toast notifications for user feedback

---

## Project Structure

```
ambulance_ucs/
├── app.py              # Flask backend server + 5 API endpoints
├── ucs.py              # Pure UCS algorithm implementation (heapq-based)
├── graph.py            # Graph builder, OSRM fetcher, Haversine calculator
├── requirements.txt    # Python dependencies
├── test_system.py      # Comprehensive system test suite
├── templates/
│   └── index.html      # Leaflet map interface + HTML layout
└── static/
    ├── map.js          # Frontend interactivity + visualizations
    └── style.css       # Responsive split-screen styling
```

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd ambulance_ucs
pip install -r requirements.txt
```

**Packages installed:**
- `flask` - Web framework
- `flask-cors` - Cross-Origin Resource Sharing
- `requests` - HTTP client for OSRM API calls

### Step 2: Run the Flask Server

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

---

## Usage Guide

### 1. **Select Emergency Location**
   - Dropdown shows 2 emergency incident locations (Adyar, T. Nagar)

### 2. **Select Destination Hospital**
   - Dropdown shows 3 hospitals (Apollo, Fortis Malar, Stanley)

### 3. **Click "Run UCS"**
   - Algorithm runs and animates exploration
   - Each node expands at 350ms intervals
   - Explored nodes turn green with checkmarks
   - Final optimal path highlights in orange with ⭐

### 4. **View Results**
   - **Optimal Route:** Complete path as node names
   - **Travel Time:** Total journey time in minutes
   - **Nodes Explored:** Count of nodes expanded vs. total
   - **Priority Queue:** Live view of frontier during execution
   - **Expansion Log:** Step-by-step log of each node expansion

### 5. **Random Emergency**
   - Click to auto-select random incident + hospital
   - Instantly runs UCS with random pair

### 6. **Reset**
   - Clears all visualizations and returns to initial state

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Serve main HTML page |
| `GET` | `/api/nodes` | Return all 12 nodes with coordinates |
| `GET` | `/api/graph` | Build & return graph with edges + OSRM durations |
| `POST` | `/api/solve` | Run UCS algorithm with start/goal nodes |
| `GET` | `/api/graph/refresh` | Force re-fetch from OSRM |

### Example API Calls

**Get all nodes:**
```bash
GET http://localhost:5000/api/nodes
```

**Get graph with edges:**
```bash
GET http://localhost:5000/api/graph
```

**Run UCS algorithm:**
```bash
POST http://localhost:5000/api/solve
Content-Type: application/json

{
  "start": "incident_1",
  "goal": "apollo"
}
```

**Response:**
```json
{
  "found": true,
  "path": ["incident_1", "mylapore", "apollo"],
  "total_cost_seconds": 888,
  "total_cost_minutes": 14.8,
  "explored_order": [
    {"node": "incident_1", "cumulative_cost": 0, "path_so_far": ["incident_1"]},
    {"node": "mylapore", "cumulative_cost": 8.3, "path_so_far": ["incident_1", "mylapore"]},
    ...
  ],
  "route_geometry": {
    "incident_1->mylapore": [[13.006, 80.248], [13.0368, 80.2676], ...],
    "mylapore->apollo": [[13.0368, 80.2676], [13.0604, 80.2496], ...]
  }
}
```

---

## Algorithm Details

### Uniform Cost Search (UCS)

UCS is an uninformed search algorithm that expands nodes in order of their path cost from the start node. It guarantees finding the **optimal lowest-cost path**.

**Key Features:**
- Uses a **priority queue (min-heap)** to explore nodes by cost
- Expands lowest-cost nodes first
- Guarantees optimal solution (if costs are non-negative)
- Complete and optimal

**Implementation:** `ucs.py`
- Uses Python's `heapq` module for efficient priority queue
- Returns: path, total cost, explored order (for animation)

### Graph Construction

The system builds a weighted graph from real road network data:

1. **Nodes** (12 locations):
   - 3 Hospitals: Apollo, Fortis Malar, Stanley
   - 7 Landmarks: Central, Egmore, T. Nagar, Adyar, Anna Nagar, Velachery, Mylapore
   - 2 Emergency incidents: Adyar, T. Nagar

2. **Edges** (20 connections):
   - Predefined realistic road topology in Chennai
   - Each edge connects two adjacent locations

3. **Edge Weights**:
   - Fetched from OSRM public API (real driving duration in seconds)
   - Fallback to Haversine distance if OSRM unavailable
   - Converted to minutes for display

### OSRM Integration

**OSRM (Open Source Routing Machine)** provides real road routing:

- **Table API**: Get travel durations between all node pairs
  - URL: `https://router.project-osrm.org/table/v1/driving/{coordinates}?sources=all&destinations=all&annotations=duration`

- **Route API**: Get detailed polyline for map visualization
  - URL: `https://router.project-osrm.org/route/v1/driving/{start};{end}?overview=full&geometries=geojson`

### Fallback: Haversine

If OSRM is unavailable:
- Calculate straight-line distance using Haversine formula
- Assume 40 km/h average speed
- Convert to duration in seconds

---

## Frontend Architecture

### Map Visualization

- **Leaflet.js** for interactive map rendering
- **OpenStreetMap** tiles (free, no authentication)
- **Custom markers** for different node types

### Marker Types

| Type | Color | Icon | Animation |
|------|-------|------|-----------|
| Hospital | Blue | H | Static |
| Incident | Red | ! | Pulsing |
| Landmark | Gray | • | Static |
| Explored | Green | ✓ | Scale in |
| Optimal Path | Orange | ★ | Glowing |

### Animation Timeline

1. **Page Load** (0ms):
   - Show spinner, fetch `/api/graph`
   - Plot all nodes on map
   - Draw edge polylines (gray dashed)
   - Populate dropdowns

2. **Run UCS** (triggered):
   - POST to `/api/solve`
   - Clear previous visualization
   - For each explored node (350ms interval):
     - Change marker to green
     - Add entry to step log
     - Update priority queue view
     - Draw path so far

3. **After Exploration** (final):
   - Draw optimal path as thick orange polylines
   - Highlight optimal path nodes with orange stars
   - Unlock Reset button

---

## Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

**Tests included:**
1. ✓ API nodes endpoint
2. ✓ Graph building with OSRM
3. ✓ UCS algorithm execution
4. ✓ Error handling for invalid nodes
5. ✓ Graph refresh endpoint

**Expected output:**
```
==================================================
AMBULANCE ROUTE OPTIMIZATION SYSTEM - TEST SUITE
==================================================
TEST 1: GET /api/nodes
  ✓ Loaded 12 nodes
TEST 2: GET /api/graph
  ✓ Graph built successfully
TEST 3: POST /api/solve (UCS Algorithm)
  ✓ UCS algorithm executed successfully
TEST 4: GET /api/solve with invalid nodes
  ✓ Invalid nodes rejected correctly
TEST 5: GET /api/graph/refresh
  ✓ Graph refresh successful

RESULTS: 5/5 tests passed
✅ ALL TESTS PASSED - System is fully operational!
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| **Nodes** | 12 |
| **Edges** | 20 (each bidirectional = 40 connections) |
| **Graph Build Time** | ~2-3 seconds (OSRM fetch) |
| **UCS Execution Time** | <100ms (finding optimal path) |
| **Animation Time** | 350ms × nodes_explored (e.g., 5 nodes = 1.75s) |
| **First Load** | ~5 seconds (OSRM fetch + map render) |
| **Subsequent Requests** | <100ms (cached graph) |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         BROWSER (Leaflet.js)                │
│  ┌──────────────────────────────────────┐  │
│  │ Map Visualization + Controls         │  │
│  │ - Split-screen (40% UI, 60% map)     │  │
│  │ - Custom markers (5 types)           │  │
│  │ - Animated polylines                 │  │
│  │ - Stats panel + Step log             │  │
│  └──────────────────────────────────────┘  │
└────────────┬────────────────────────────────┘
             │ HTTP / JSON
             ▼
┌─────────────────────────────────────────────┐
│         FLASK BACKEND (app.py)              │
│  ┌──────────────────────────────────────┐  │
│  │ 5 API Endpoints                      │  │
│  │ - GET /api/nodes                     │  │
│  │ - GET /api/graph                     │  │
│  │ - POST /api/solve (UCS)              │  │
│  │ - GET /api/graph/refresh             │  │
│  └──────────────────────────────────────┘  │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴────────┬─────────────┐
    ▼                 ▼             ▼
┌────────┐      ┌──────────┐  ┌────────┐
│ ucs.py │      │ graph.py │  │ nodes  │
│  UCS   │      │  Graph   │  │ data   │
│  algo  │      │ builder  │  │        │
└────────┘      └────┬─────┘  └────────┘
                     │
            ┌────────┴─────────┐
            ▼                  ▼
        ┌───────────┐   ┌──────────────┐
        │   OSRM    │   │  Haversine   │
        │   API     │   │  Fallback    │
        │  (live)   │   │  (backup)    │
        └───────────┘   └──────────────┘
```

---

## Example Scenario

**Emergency: Accident in Adyar → Get to Apollo Hospital**

1. User selects:
   - Start: "Emergency - Adyar" (incident_1)
   - Goal: "Apollo Hospital"

2. Backend executes:
   - UCS explores frontier by cost
   - Priority queue: [(0, incident_1)]
   - Pop incident_1, explore neighbors
   - Push (8.3 min, adyar) and (7.1 min, mylapore)
   - Pop mylapore (lower cost), explore neighbors
   - Find apollo at cost 14.8 min total

3. Frontend animates:
   - Expands incident_1 (green ✓)
   - Waits 350ms
   - Expands adyar (green ✓)
   - Waits 350ms
   - Expands mylapore (green ✓)
   - Waits 350ms
   - Expands apollo (green ✓)
   - Draws orange ⭐ path: adyar → mylapore → apollo
   - Shows: "14.8 minutes"

---

## Deployment Considerations

### For Production

1. **Use Gunicorn/uWSGI** instead of Flask dev server
2. **Setup nginx** as reverse proxy
3. **Enable HTTPS/SSL** for API security
4. **Implement database** (Redis/PostgreSQL) to cache OSRM responses permanently
5. **Add rate limiting** for OSRM API calls
6. **Set up monitoring** (error logs, performance metrics)

### Environment Variables

```bash
FLASK_ENV=production
FLASK_DEBUG=0
OSRM_URL=https://router.project-osrm.org  # Configurable
PORT=5000
```

---

## Troubleshooting

### Issue: "OSRM requests failing"
**Solution:** System automatically falls back to Haversine. Check internet connection. OSRM has public rate limits.

### Issue: "Graph not loading on page"
**Solution:** Check browser console for errors. Ensure Flask server is running on port 5000.

### Issue: "Slow animation"
**Solution:** This is normal. 350ms per node ensures readability. Adjust in `map.js` if needed.

### Issue: "Port 5000 already in use"
**Solution:** Kill existing process or change port in `app.py` (line: `app.run(port=5000)`)

---

## License

Open source - use freely for educational and commercial purposes.

---

## Author

Built with ❤️ for ambulance route optimization in smart cities.

**Technologies:** Flask, Python, UCS Algorithm, Leaflet.js, OSRM, OpenStreetMap

---

## Future Enhancement Ideas

- [ ] Multi-ambulance routing (simultaneous optimization)
- [ ] Real-time traffic integration (TomTom/HERE APIs)
- [ ] Database persistence for route history
- [ ] Mobile app (React Native / Flutter)
- [ ] Real emergency dispatch system integration
- [ ] Predictive routing based on historical data
- [ ] Custom edge weights (time of day, traffic patterns)
- [ ] Alternative algorithm comparison (A*, Dijkstra)

---

## Support

For issues or questions, refer to the test suite (`test_system.py`) or API documentation above.
