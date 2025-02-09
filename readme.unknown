// Initialize the map with default view
var map = L.map('map').setView([20.5937, 78.9629], 5); // Default to India

// Google Maps Layers
var googleLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    attribution: 'Map data &copy; <a href="https://www.google.com/maps">Google Maps</a>'
}).addTo(map);

var satelliteLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
    attribution: 'Map data &copy; <a href="https://www.google.com/maps">Google Maps</a>'
});

var baseMaps = {
    "Google Map": googleLayer,
    "Satellite": satelliteLayer
};

L.control.layers(baseMaps).addTo(map);

// Add Geocoder
L.Control.geocoder().addTo(map);

// API URL for pothole data
const apiUrl = 'http://127.0.0.1:5000/api/potholes';
const loadingElement = document.getElementById('loading');
let watchId = null;
let bestPosition = null; // Store the best available position
let routingControl = null;
const geocodeService = 'https://nominatim.openstreetmap.org/search';

// Function to show/hide loading animation
function showLoading(show) {
    if (loadingElement) {
        loadingElement.style.display = show ? 'block' : 'none';
    }
}

// Fetch pothole data and display markers
showLoading(false);
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.success && data.data.length > 0) {
            data.data.forEach(pothole => {
                const { latitude, longitude } = pothole;
                L.circleMarker([latitude, longitude], {
                    radius: 8,
                    color: '#FF4500',
                    fillColor: '#FF4500',
                    fillOpacity: 0.7
                }).addTo(map)
                    .bindPopup(`<strong>Pothole detected!</strong><br>Latitude: ${latitude}<br>Longitude: ${longitude}`);
            });
        } else {
            alert('No pothole data available!');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Error fetching pothole data:', error);
        alert('Failed to fetch pothole data from the server.');
    });

// Function to continuously update user location
// Function to continuously update user location and route
async function useCurrentLocation() {
    var fromInput = document.getElementById('from');

    if (!navigator.geolocation) {
        alert("Geolocation is not supported by this browser.");
        return;
    }

    fromInput.value = "Fetching location...";

    try {
        if (navigator.permissions) {
            let permissionStatus = await navigator.permissions.query({ name: "geolocation" });

            if (permissionStatus.state === "denied") {
                alert("Location permission is denied. Please allow location access in browser settings.");
                fromInput.value = "";
                return;
            }
        }

        watchId = navigator.geolocation.watchPosition(
            async function (position) {
                const { latitude: lat, longitude: lon, accuracy } = position.coords;

                console.log(`Live Location Update: Lat: ${lat}, Lon: ${lon}, Accuracy: ${accuracy} meters`);

                // Update best available position dynamically
                bestPosition = { lat, lon, accuracy };

                try {
                    let response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&addressdetails=1`);
                    let data = await response.json();

                    if (data && data.display_name) {
                        fromInput.value = data.display_name;
                    } else {
                        fromInput.value = `Lat: ${lat}, Lon: ${lon}`;
                    }

                    // Recalculate route dynamically
                    calculateRoute();

                } catch (error) {
                    fromInput.value = "Unable to fetch address";
                    console.error("Error fetching location:", error);
                }
            },
            function (error) {
                console.error("Geolocation error:", error);
                alert("Could not fetch location. Please try again.");
                fromInput.value = "";
            },
            {
                enableHighAccuracy: true,
                timeout: 2000,
                maximumAge: 2000
            },
            function stopTracking() {
                if (watchId !== null) {
                    navigator.geolocation.clearWatch(watchId);
                    console.log("Location tracking stopped.");
                    alert("Location tracking stopped.");
                    watchId = null; // Reset watchId
                    
                }
            }
        );
    } catch (err) {
        console.error("Error requesting location permissions:", err);
        alert("Could not request location permissions. Please check browser settings.");
    }
    

}

// Function to calculate and update route dynamically
function calculateRoute() {
    if (!map) {
        console.error("Map is not initialized.");
        alert("Error: Map is not loaded. Please check if Leaflet is included.");
        return;
    }

    var from = document.getElementById('from').value;
    var to = document.getElementById('to').value;

    if (!to) {
        alert("Please enter a destination location.");
        return;
    }

    showLoading(false);

     // Remove previous route before adding a new one
     if (routingControl) {
        map.removeControl(routingControl);
        routingControl = null; // Reset routing control
    }


    function processRouting(fromLatLng, toLatLng) {
        // Remove the previous route before adding a new one
        if (routingControl) {
            map.removeControl(routingControl);
        }
         // Remove previous 'from' marker if it exists
        if (fromMarker) {
            map.removeLayer(fromMarker);
            fromMarker = null;
        }
    
        // Define a custom car icon
        var carIcon = L.icon({
            iconUrl: "C:/Users/Admin/OneDrive/Desktop/last Map/Last Final Map/car logo.png", // Ensure the path is correct
            iconSize: [60, 60],  // Adjust size as needed
            iconAnchor: [20, 20], // Center the icon properly
            popupAnchor: [0, -20] 
        });
    
        // Add a marker at the fromLocation with the custom car icon
        var fromMarker = L.marker(fromLatLng, { icon: carIcon }).addTo(map);
    
        // Create routing control
        routingControl = L.Routing.control({
            waypoints: [
                L.latLng(fromLatLng),
                L.latLng(toLatLng)
            ],
            routeWhileDragging: false,
            draggableWaypoints: false,
            addWaypoints: false,
            showAlternatives: true,
            createMarker: function(i, waypoint, n) {
                if (i === 0) { 
                    // Use the custom car icon for the starting location
                    return fromMarker;
                } else {
                    // Default marker for the destination
                    return L.marker(waypoint.latLng);
                }
            },
            altLineOptions: {
                styles: [
                    { color: 'black', opacity: 0.15, weight: 9 },
                    { color: 'white', opacity: 0.8, weight: 6 },
                    { color: 'blue', opacity: 0.5, weight: 2 }
                ]
            }
        }).addTo(map);
    }
    
    if (bestPosition) {
        let fromLatLng = [bestPosition.lat, bestPosition.lon];
        fetchGeocode(to).then(toLatLng => {
            if (toLatLng) processRouting(fromLatLng, toLatLng);
        });
    }

    else if (from) {
        // If the user manually enters a 'from' location, fetch its coordinates
        fetchGeocode(from).then(fromLatLng => {
            if (fromLatLng) {
                fetchGeocode(to).then(toLatLng => {
                    if (toLatLng) {
                        processRouting(fromLatLng, toLatLng);
                    } else {
                        alert("Geocoding failed for the destination. Please check the input.");
                    }
                });
            } else {
                alert("Geocoding failed for the 'from' location. Please check the input.");
            }
        });
    }

     else {
        alert("Waiting for location update...");
        showLoading(false);
    }
}

// Function to fetch geocode data for an address
async function fetchGeocode(address) {
    try {
        let response = await fetch(`${geocodeService}?q=${encodeURIComponent(address)}&format=json`);
        let data = await response.json();
        return data.length > 0 ? [data[0].lat, data[0].lon] : null;
    } catch (err) {
        console.error(`Error fetching geocoding data for ${address}:`, err);
        alert(`An error occurred while fetching the location: ${address}`);
        return null;
    }
}

// Function to stop watching location updates
function stopTracking() {
    if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
        console.log("Location tracking stopped.");
        alert("Location tracking stopped.");
        watchId = null;  // Reset watchId
        bestPosition = null;  // ✅ Reset stored GPS location
    }
}
