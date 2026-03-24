// Global state
let map;
let markers = {};
let polylines = [];
let currentAlgorithmState = {
    running: false,
    paused: false,
    currentStepIndex: 0,
    exploredOrder: [],
    path: [],
    startNode: null,
    goalNode: null
};
let animationTimer = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    initializeMap();
    await loadGraphData();
    setupEventListeners();
});

// Initialize Leaflet map
function initializeMap() {
    const chennaiBounds = [13.0827, 80.2707];
    map = L.map('map').setView(chennaiBounds, 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

// Load graph data from backend
async function loadGraphData() {
    showSpinner(true);
    try {
        const response = await fetch('/api/graph');
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Failed to load graph');
        }
        
        appData.nodes = data.nodes;
        appData.edges = data.edges;
        appData.graph = data.graph;
        
        plotNodes();
        drawEdges();
        populateSelects();
        showSpinner(false);
    } catch (error) {
        console.error('Error loading graph:', error);
        showToast(`Error: ${error.message}`);
        showSpinner(false);
    }
}

// Plot all nodes as markers
function plotNodes() {
    for (const [nodeId, nodeData] of Object.entries(appData.nodes)) {
        const icon = createCustomIcon(nodeData.type);
        const marker = L.marker([nodeData.lat, nodeData.lng], { icon })
            .bindPopup(`<strong>${nodeData.name}</strong><br>Type: ${nodeData.type}`)
            .addTo(map);
        
        markers[nodeId] = {
            marker: marker,
            type: nodeData.type,
            lat: nodeData.lat,
            lng: nodeData.lng,
            name: nodeData.name
        };
    }
}

// Create custom icon based on node type
function createCustomIcon(type) {
    let htmlContent = '';
    let iconClass = '';
    
    switch (type) {
        case 'hospital':
            htmlContent = 'H';
            iconClass = 'marker-icon-hospital';
            break;
        case 'incident':
            htmlContent = '!';
            iconClass = 'marker-icon-incident';
            break;
        case 'landmark':
            htmlContent = '•';
            iconClass = 'marker-icon-landmark';
            break;
        default:
            htmlContent = '•';
            iconClass = 'marker-icon-landmark';
    }
    
    return L.divIcon({
        html: `<div class="${iconClass}">${htmlContent}</div>`,
        className: 'custom-marker',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        popupAnchor: [0, -16]
    });
}

// Draw edges as polylines
function drawEdges() {
    appData.edges.forEach(([node1, node2]) => {
        if (appData.nodes[node1] && appData.nodes[node2]) {
            const n1 = appData.nodes[node1];
            const n2 = appData.nodes[node2];
            
            const polyline = L.polyline(
                [[n1.lat, n1.lng], [n2.lat, n2.lng]],
                {
                    color: '#bbb',
                    weight: 2,
                    opacity: 0.5,
                    dashArray: '5, 5'
                }
            ).addTo(map);
            
            // Add tooltip with travel time
            const duration = calculateDuration(node1, node2);
            polyline.bindTooltip(`${node1} → ${node2}<br>${duration.toFixed(1)} seconds`);
            
            polylines.push(polyline);
        }
    });
}

// Calculate travel duration between two nodes
function calculateDuration(node1, node2) {
    const graph = appData.graph;
    if (graph[node1]) {
        for (const [neighbor, duration] of graph[node1]) {
            if (neighbor === node2) {
                return duration;
            }
        }
    }
    return 0;
}

// Populate dropdown selects
function populateSelects() {
    const startSelect = document.getElementById('start-node');
    const goalSelect = document.getElementById('goal-node');
    
    // Filter incidents for start
    const incidents = Object.entries(appData.nodes).filter(([, data]) => data.type === 'incident');
    incidents.forEach(([id, data]) => {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = data.name;
        startSelect.appendChild(option);
    });
    
    // Filter hospitals for goal
    const hospitals = Object.entries(appData.nodes).filter(([, data]) => data.type === 'hospital');
    hospitals.forEach(([id, data]) => {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = data.name;
        goalSelect.appendChild(option);
    });
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('btn-run').addEventListener('click', runUCS);
    document.getElementById('btn-step').addEventListener('click', stepManual);
    document.getElementById('btn-reset').addEventListener('click', resetMap);
    document.getElementById('btn-random').addEventListener('click', randomEmergency);
}

// Run UCS algorithm
async function runUCS() {
    const startNode = document.getElementById('start-node').value;
    const goalNode = document.getElementById('goal-node').value;
    
    if (!startNode || !goalNode) {
        showToast('Please select both emergency location and hospital');
        return;
    }
    
    if (startNode === goalNode) {
        showToast('Start and goal must be different');
        return;
    }
    
    // Disable buttons during execution
    document.getElementById('btn-run').disabled = true;
    document.getElementById('btn-step').disabled = true;
    
    try {
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start: startNode, goal: goalNode })
        });
        
        const result = await response.json();
        
        if (!result.found) {
            showToast('No path found between selected nodes');
            return;
        }
        
        // Store state for animation
        currentAlgorithmState.exploredOrder = result.explored_order;
        currentAlgorithmState.path = result.path;
        currentAlgorithmState.startNode = startNode;
        currentAlgorithmState.goalNode = goalNode;
        currentAlgorithmState.running = true;
        currentAlgorithmState.currentStepIndex = 0;
        
        // Clear previous markers and polylines
        clearPreviousVisualization();
        
        // Update stats
        updateStats(result);
        
        // Animate exploration
        animateExploration(result);
        
    } catch (error) {
        console.error('Error running UCS:', error);
        showToast(`Error: ${error.message}`);
    } finally {
        document.getElementById('btn-run').disabled = false;
        document.getElementById('btn-step').disabled = false;
    }
}

// Animate exploration step by step
async function animateExploration(result) {
    const exploredOrder = result.explored_order;
    
    for (let i = 0; i < exploredOrder.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 350)); // 350ms interval
        
        const step = exploredOrder[i];
        const nodeId = step.node;
        
        // Update marker to explored (green)
        if (markers[nodeId]) {
            const icon = L.divIcon({
                html: '<div class="marker-icon-explored">✓</div>',
                className: 'custom-marker',
                iconSize: [20, 20],
                iconAnchor: [10, 10],
                popupAnchor: [0, -16]
            });
            markers[nodeId].marker.setIcon(icon);
        }
        
        // Add to step log
        addStepLog(step, i);
        
        // Update priority queue display
        updatePriorityQueue(exploredOrder, i);
        
        // Draw path so far as light polyline
        if (step.path_so_far.length > 1) {
            const pathCoords = step.path_so_far.map(nodeId => {
                const node = appData.nodes[nodeId];
                return [node.lat, node.lng];
            });
            
            const polyline = L.polyline(pathCoords, {
                color: '#4caf50',
                weight: 2,
                opacity: 0.3,
                dashArray: '10, 5'
            }).addTo(map);
            polylines.push(polyline);
        }
        
        currentAlgorithmState.currentStepIndex = i;
    }
    
    // Draw final optimal path
    await drawOptimalPath(result.path, result.route_geometry);
    
    // Enable reset button
    document.getElementById('btn-reset').disabled = false;
}

// Draw optimal path on map
async function drawOptimalPath(path, routeGeometry) {
    for (let i = 0; i < path.length - 1; i++) {
        const segment = `${path[i]}->${path[i + 1]}`;
        const coords = routeGeometry[segment] || [[appData.nodes[path[i]].lat, appData.nodes[path[i]].lng], [appData.nodes[path[i + 1]].lat, appData.nodes[path[i + 1]].lng]];
        
        const polyline = L.polyline(coords, {
            color: '#ff9800',
            weight: 4,
            opacity: 0.9,
            lineJoin: 'round'
        }).addTo(map);
        
        polylines.push(polyline);
    }
    
    // Highlight optimal path nodes in orange
    path.forEach(nodeId => {
        if (markers[nodeId]) {
            const icon = L.divIcon({
                html: '<div class="marker-icon-optimal">★</div>',
                className: 'custom-marker',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            });
            markers[nodeId].marker.setIcon(icon);
        }
    });
}

// Update statistics panel
function updateStats(result) {
    const pathStr = result.path.map(id => appData.nodes[id].name).join(' → ');
    document.getElementById('stat-path').textContent = pathStr || '—';
    document.getElementById('stat-time').textContent = `${result.total_cost_minutes.toFixed(1)} min`;
    document.getElementById('stat-explored').textContent = `${result.explored_order.length} / ${Object.keys(appData.nodes).length}`;
}

// Add entry to step log
function addStepLog(step, index) {
    const stepLog = document.getElementById('step-log');
    
    if (stepLog.querySelector('em')) {
        stepLog.innerHTML = '';
    }
    
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = `Step ${index + 1}: Explored "${appData.nodes[step.node]?.name}" (Cost: ${step.cumulative_cost} min)`;
    stepLog.appendChild(entry);
    stepLog.scrollTop = stepLog.scrollHeight;
}

// Update priority queue display
function updatePriorityQueue(exploredOrder, currentIndex) {
    const queueDiv = document.getElementById('priority-queue');
    queueDiv.innerHTML = '';
    
    // Show top 5 items from explored order
    const startIdx = Math.max(0, currentIndex - 2);
    const endIdx = Math.min(exploredOrder.length, currentIndex + 3);
    
    for (let i = startIdx; i < endIdx; i++) {
        const step = exploredOrder[i];
        const item = document.createElement('div');
        item.className = 'queue-item';
        if (i === currentIndex) item.className += ' current';
        item.textContent = `${appData.nodes[step.node]?.name} (${step.cumulative_cost} min)`;
        queueDiv.appendChild(item);
    }
}

// Manual step through exploration
function stepManual() {
    // TODO: Implement manual step functionality
}

// Reset map to initial state
function resetMap() {
    clearPreviousVisualization();
    document.getElementById('step-log').innerHTML = '<p><em>No algorithm run yet</em></p>';
    document.getElementById('priority-queue').innerHTML = '<em>Queue empty</em>';
    document.getElementById('stat-path').textContent = '—';
    document.getElementById('stat-time').textContent = '—';
    document.getElementById('stat-explored').textContent = '0 / 12';
    document.getElementById('btn-reset').disabled = true;
    
    currentAlgorithmState = {
        running: false,
        paused: false,
        currentStepIndex: 0,
        exploredOrder: [],
        path: [],
        startNode: null,
        goalNode: null
    };
    
    // Redraw all nodes as original markers
    for (const [nodeId, markerData] of Object.entries(markers)) {
        const nodeInfo = appData.nodes[nodeId];
        const icon = createCustomIcon(nodeInfo.type);
        markerData.marker.setIcon(icon);
    }
}

// Clear previous visualization
function clearPreviousVisualization() {
    polylines.forEach(polyline => map.removeLayer(polyline));
    polylines = [];
}

// Random emergency selection
async function randomEmergency() {
    const incidents = Object.entries(appData.nodes).filter(([, data]) => data.type === 'incident');
    const hospitals = Object.entries(appData.nodes).filter(([, data]) => data.type === 'hospital');
    
    if (incidents.length === 0 || hospitals.length === 0) {
        showToast('Not enough incidents or hospitals available');
        return;
    }
    
    const randomIncident = incidents[Math.floor(Math.random() * incidents.length)][0];
    const randomHospital = hospitals[Math.floor(Math.random() * hospitals.length)][0];
    
    document.getElementById('start-node').value = randomIncident;
    document.getElementById('goal-node').value = randomHospital;
    
    await runUCS();
}

// Show/hide loading spinner
function showSpinner(show) {
    const spinner = document.getElementById('spinner');
    if (show) {
        spinner.classList.remove('hidden');
    } else {
        spinner.classList.add('hidden');
    }
}

// Show toast notification
function showToast(message) {
    const toast = document.getElementById('error-toast');
    const messageEl = document.getElementById('toast-message');
    messageEl.textContent = message;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
