var longitudeRIT = -77.675250;
var latitudeRIT = 43.084132;

const bounds = [
    [-77.688972, 43.072019], // Southwest coordinates
    [-77.663638, 43.092922] // Northeast coordinates
];

const map = (window.map = new maplibregl.Map({
    container: 'map',
    zoom: 14.85,
    center: [longitudeRIT, latitudeRIT],
    pitch: 0,
    hash: true,
    style: {
        version: 8,
        sources: {
            osm: {
                type: 'raster',
                tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
                tileSize: 256,
                attribution: '&copy; OpenStreetMap Contributors',
                maxzoom: 50
            },
            // Use a different source for terrain and hillshade layers, to improve render quality
            terrainSource: {
                type: 'raster-dem',
                url: 'https://demotiles.maplibre.org/terrain-tiles/tiles.json',
                tileSize: 256
            },
            hillshadeSource: {
                type: 'raster-dem',
                url: 'https://demotiles.maplibre.org/terrain-tiles/tiles.json',
                tileSize: 256
            }
        },
        layers: [
            {
                id: 'osm',
                type: 'raster',
                source: 'osm'
            },
            {
                id: 'hills',
                type: 'hillshade',
                source: 'hillshadeSource',
                layout: {visibility: 'visible'},
                paint: {'hillshade-shadow-color': '#473B24'}
            }
        ],
        terrain: {
            source: 'terrainSource',
            exaggeration: 1
        }
    },
    maxZoom: 18,
    maxPitch: 85,
    maxBounds: bounds
}));

const geojson = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'properties': {
                'message': 'Vehicle_1: (-77.681361, 43.081066)',
                'iconSize': [60, 60]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [-77.681361, 43.081066]
            },
            'image': {
                'path': `url(/E.png)`
            }
        },
        {
            'type': 'Feature',
            'properties': {
                'message': 'Vehicle_2: (-77.679376, 43.082474)',
                'iconSize': [60, 60]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [-77.679376, 43.082474]
            },
            'image': {
                'path': `url(/N.png)`
            }
        }
    ]
};


// add markers to map
geojson.features.forEach((marker) => {
    // create a DOM element for the marker
    const el = document.createElement('div');
    el.className = 'marker';
    el.style.backgroundImage = `${marker.image.path}`;
    el.style.width = `${marker.properties.iconSize[0]}px`;
    el.style.height = `${marker.properties.iconSize[1]}px`;
    el.style.backgroundRepeat = `no-repeat`;

    el.addEventListener('click', () => {
        window.alert(marker.properties.message);
    });

    // add marker to map
    new maplibregl.Marker({element: el})
        .setLngLat(marker.geometry.coordinates)
        .addTo(map);
});

map.scrollZoom.disable();
map.doubleClickZoom.disable();