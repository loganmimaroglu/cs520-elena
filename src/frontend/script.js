const data = {
    "orig": "141 Echo Avenue, Oakland, CA 94611",
    "dest": "1123 Oakland Avenue, Piedmont, CA 94611",
    "max_min": "max",
    "variance": "1.1"
}

const options = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
}

const url = 'http://127.0.0.1:3000/route'



window.onload = async function getRoute() {
    const response = await fetch(url, options);

    const route = await response.json();

    console.log(route[0]);
    console.log(route)

    mapboxgl.accessToken = 'pk.eyJ1IjoibG1pbWFyb2dsdSIsImEiOiJjbGJlZmNxMnowYXlwM25uazJkZjBkenAzIn0.Hs-PwwNjmXbxpbqzHIZaNw';

    const map = new mapboxgl.Map({
        container: 'map',
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/streets-v12',
        center: route[0],
        zoom: 14
    });

    const directions = new MapboxDirections({
      unit: 'metric',
      profile: 'mapbox/driving',
    });

    map.on('load', () => {
        map.addSource('route', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'LineString',
                    'coordinates': route
                }
            }
        });
        map.addLayer({
            'id': 'route',
            'type': 'line',
            'source': 'route',
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
            },
            'paint': {
                'line-color': '#1982FC',
                'line-width': 8
            }
        });
    });

    map.addControl(directions, 'top-left');

}


// document.addEventListener('DOMContentLoaded', function() {
//     fetch(url, options)
//         .then(response => response.json())
//         .then(data => console.log(data))
//         .catch(error => console.error(error))
// })