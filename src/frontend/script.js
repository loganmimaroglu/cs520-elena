// Add your Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoibG1pbWFyb2dsdSIsImEiOiJjbGJlZmNxMnowYXlwM25uazJkZjBkenAzIn0.Hs-PwwNjmXbxpbqzHIZaNw';

// Initialize a map
const map = new mapboxgl.Map({
  container: 'map', // Specify the container ID
  style: 'mapbox://styles/mapbox/streets-v12', // Specify which map style to use
  center: [-122.247604, 37.826250], // Specify the starting position
  zoom: 14.5, // Specify the starting zoom
});

// Add zoom and rotation controls to the map.
map.addControl(new mapboxgl.NavigationControl());

// Add geolocate control to the map.
map.addControl(
  new mapboxgl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true
    },
    // When active the map will receive updates to the device's location as it changes.
    trackUserLocation: true,
    // Draw an arrow next to the location dot to indicate which direction the device is heading.
    showUserHeading: true
  })
);


/**
 * This function is responsible for making the request to the backend to get the coordinates of the route
 * @returns route - list of coordinates of the route
 */
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

/**
 * This function is responsible for sending the coords list to other functions so that the path can be added to the map
 * @returns null
 */
async function updateRoute() {
  // check for empty values - throws and error if required values are not entered
  if (document.getElementById('starting-address').value === '' || document.getElementById('ending-address').value === '' || document.getElementById('starting-city').value === '' || document.getElementById('ending-city').value === '' || document.getElementById('starting-state').value === '' || document.getElementById('ending-state').value === '' || document.getElementById('starting-zip').value === '' || document.getElementById('ending-zip').value === '' || document.getElementById('minmax').value === '' || document.getElementById('variance').value === '') {
    document.getElementById('Error').innerHTML = '**Please enter all the required values';
  } else {
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
}

/**
 * This function is responsible for sending a request to the backend to get the routes
 * @parameters coordinates - the coordinates of the route
 * @parameters profile - the mode of transportation to be used for the route (walking, driving, cycling)
 * @returns null
 */
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

/**
 * This function is responsible for adding a new layer to the map which is our calculated route
 * @parameters coords - the route to be taken to reach destination
 * @returns null
 */
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

/**
 * This function is responsible for adding a new layer to the map which is our calculated route
 * @parameters coords - the coordinates of the route
 * @returns null
 */
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

/**
 * This function is responsible for resetting the entire map including all routes and input boxes
 * @returns null
 */
function removeRoute() {
  if (!map.getSource('route')) return;
  map.removeLayer('route');
  map.removeSource('route');
  document.getElementById('directions').innerHTML = '';
  document.getElementById('starting-address').value = '';
  document.getElementById('ending-address').value = '';
  document.getElementById('starting-city').value = '';
  document.getElementById('ending-city').value = '';
  document.getElementById('starting-state').value = '';
  document.getElementById('ending-state').value = '';
  document.getElementById('starting-zip').value = '';
  document.getElementById('ending-zip').value = '';
  document.getElementById('minmax').value = '';
  document.getElementById('variance').value = '';
}

// Add event listeners
document.getElementById("go").addEventListener("click", updateRoute)
document.getElementById("reset").addEventListener("click", removeRoute)
