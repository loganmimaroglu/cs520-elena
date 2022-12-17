// Add your Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoibG1pbWFyb2dsdSIsImEiOiJjbGJlZmNxMnowYXlwM25uazJkZjBkenAzIn0.Hs-PwwNjmXbxpbqzHIZaNw';
const map = new mapboxgl.Map({
  container: 'map', // Specify the container ID
  style: 'mapbox://styles/mapbox/streets-v12', // Specify which map style to use
  center: [-122.247604, 37.826250], // Specify the starting position
  zoom: 14.5, // Specify the starting zoom
});

async function getRoute() {
  const data = {
    "orig": document.getElementById('starting-address').value + ", " + document.getElementById('starting-city').value + ", " + document.getElementById('starting-state').value + " " + document.getElementById('starting-zip').value,
    "dest": document.getElementById('ending-address').value + ", " + document.getElementById('ending-city').value + ", " + document.getElementById('ending-state').value + " " + document.getElementById('ending-zip').value,
    'max_min': document.getElementById('minmax').value,
    'variance': document.getElementById('variance').value
  }

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }

  const url = 'http://127.0.0.1:3000/route';

  const response = await fetch(url, options);

  const route = await response.json();

  return route;
}

// Use the coordinates you drew to make the Map Matching API request
async function updateRoute() {
  // Set the profile
  const profile = 'walking';
  // Get the route from our properity routing algo
  const coords = await getRoute();
  let newCoords = ""
  for (let i = 0; i < coords.length; i++) {
    if (coords.length - 1 !== i) {
      newCoords += `${coords[i][0]},${coords[i][1]};`
    } else {
      newCoords += `${coords[i][0]},${coords[i][1]}`
    }
  }
  console.log(newCoords)
  getMatch(newCoords, profile);
}

// Make a Map Matching request
async function getMatch(coordinates, profile) {
  // Create the query
  const query = await fetch(
    `https://api.mapbox.com/matching/v5/mapbox/${profile}/${coordinates}?geometries=geojson&steps=true&access_token=${mapboxgl.accessToken}`,
    { method: 'GET' }
  );
  const response = await query.json();
  // Handle errors
  if (response.code !== 'Ok') {
    alert(
      `${response.code} - ${response.message}.\n\nFor more information: https://docs.mapbox.com/api/navigation/map-matching/#map-matching-api-errors`
    );
    return;
  }
  // Get the coordinates from the response
  const coords = response.matchings[0].geometry;
  console.log(coords);
  // Code from the next step will go here
  addRoute(coords)
  getInstructions(response.matchings[0])
}

function getInstructions(data) {
  // Target the sidebar to add the instructions
  const directions = document.getElementById('directions');
  let tripDirections = '';
  // Output the instructions for each step of each leg in the response object
  for (const leg of data.legs) {
    const steps = leg.steps;
    for (const step of steps) {
      tripDirections += `<li>${step.maneuver.instruction}</li>`;
    }
  }
  directions.innerHTML = `<p><strong>Trip duration: ${Math.floor(
    data.duration / 60
  )} min.</strong></p><ol>${tripDirections}</ol>`;
}

// Draw the Map Matching route as a new layer on the map
function addRoute(coords) {
  // If a route is already loaded, remove it
  if (map.getSource('route')) {
    map.removeLayer('route');
    map.removeSource('route');
  } else {
    // Add a new layer to the map
    map.addLayer({
      id: 'route',
      type: 'line',
      source: {
        type: 'geojson',
        data: {
          type: 'Feature',
          properties: {},
          geometry: coords
        }
      },
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#1982FC',
        'line-width': 8,
        'line-opacity': 0.8
      }
    });
  }
}

// If the user clicks the delete button, remove the layer if it exists
function removeRoute() {
  if (!map.getSource('route')) return;
  map.removeLayer('route');
  map.removeSource('route');
  document.getElementById('directions').innerHTML = '';
  document.getElementById('startingAddress').value = '';
  document.getElementById('endingAddress').value = '';
  document.getElementById('minmax').value = '';
  document.getElementById('variance').value = '';
}

document.getElementById("go").addEventListener("click", updateRoute)
document.getElementById("reset").addEventListener("click", removeRoute)