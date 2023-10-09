/**
 * Load OpenStreetMap focused on RIT campus.
 *
 * This code loads a map centered on the RIT campus and sets bounds to keep the map located at/around RIT. Scrolling and
 * zooming is locked out to keep the map on-location.
 */

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
    'features': []
};

map.scrollZoom.disable();
map.doubleClickZoom.disable();