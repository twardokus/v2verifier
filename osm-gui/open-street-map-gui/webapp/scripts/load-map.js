/**
 * Load OpenStreetMap focused on RIT campus.
 *
 * This code loads a map centered on the RIT campus and sets bounds to keep the map located at/around RIT. Scrolling and
 * zooming is locked out to keep the map on-location.
 */

mapboxgl.accessToken = mapboxkey;
const map = new mapboxgl.Map({
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-77.688972, 43.072019],
    zoom: 15.5,
    pitch: 45,
    bearing: -17.6,
    container: 'map',
    antialias: true,
});

map.on('style.load', () => {
    // Insert the layer beneath any symbol layer.
    const layers = map.getStyle().layers;
    const labelLayerId = layers.find(
        (layer) => layer.type === 'symbol' && layer.layout['text-field']
    ).id;

    // The 'building' layer in the Mapbox Streets
    // vector tileset contains building height data
    // from OpenStreetMap.
    map.addLayer(
        {
            'id': 'add-3d-buildings',
            'source': 'composite',
            'source-layer': 'building',
            'filter': ['==', 'extrude', 'true'],
            'type': 'fill-extrusion',
            'minzoom': 15,
            'paint': {
                'fill-extrusion-color': '#aaa',

                // Use an 'interpolate' expression to
                // add a smooth transition effect to
                // the buildings as the user zooms in.
                'fill-extrusion-height': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    15,
                    0,
                    15.05,
                    ['get', 'height']
                ],
                'fill-extrusion-base': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    15,
                    0,
                    15.05,
                    ['get', 'min_height']
                ],
                'fill-extrusion-opacity': 0.6
            }
        },
        labelLayerId
    );
          if (api.buildings) {
            if (!map.getLayer("3d-buildings")) {
              map.addLayer(createCompositeLayer("3d-buildings"));
            }
          }
    // map.addLayer(createCustomLayer('3d-model'), 'waterway-label');
});

window.tb = new Threebox(
    map,
    map.getCanvas().getContext('webgl'), {
        realSunlight: true,
        enableTooltips: true
    }
);
tb.setSunlight(new Date(2020, 6, 19, 23), map.getCenter());

function createCustomLayer(layerName) {
    let model;
    //create the layer
    let customLayer3D = {
        id: layerName,
        type: 'custom',
        renderingMode: '3d',
        onAdd: function(map, gl) {

            let options = {
                type: 'mtl', //model type
                obj: 'https://unpkg.com/threebox-plugin/examples/models/Truck' + '.obj', //model .obj url
                mtl: 'https://unpkg.com/threebox-plugin/examples/models/Truck' + '.mtl', //model .mtl url
                units: 'meters', // in meters
                scale: 3, //x3 times is real size for this model
                rotation: {
                    x: 90,
                    y: 0,
                    z: 0
                }, //default rotation
                anchor: 'top'
            }
            tb.loadObj(options, function(model) {
                truck = model.setCoords([-77.679372, 43.080256, 0]);
                truck.setRotation({
                    x: 0,
                    y: 0,
                    z: -38
                }); //turn it to the initial street way
                truck.castShadow = false;
                truck.selected = false;

                tb.add(truck);

            });


        },
        render: function(gl, matrix) {
            tb.update();
        }
    };
    return customLayer3D;

};

function createCompositeLayer(layerId) {
    let layer = {
        'id': layerId,
        'source': "composite",
        'source-layer': "building",
        'filter': ['==', 'extrude', 'true'],
        'type': 'fill-extrusion',
        'minzoom': 12,
        'paint': {
            'fill-extrusion-color': [
                'case',
                ['boolean', ['feature-state', 'select'], false],
                "red",
                ['boolean', ['feature-state', 'hover'], false],
                "lightblue",
                '#aaa'
            ],

            // use an 'interpolate' expression to add a smooth transition effect to the
            // buildings as the user zooms in
            'fill-extrusion-height': [
                'interpolate',
                ['linear'],
                ['zoom'],
                12,
                0,
                12 + 0.05,
                ['get', 'height']
            ],
            'fill-extrusion-base': [
                'interpolate',
                ['linear'],
                ['zoom'],
                12,
                0,
                12 + 0.05,
                ['get', 'min_height']
            ],
            'fill-extrusion-opacity': 0.9
        }
    };
    return layer;
}

let api = {
          buildings: true,
          acceleration: 5,
          inertia: 3
        };

//
// var longitudeRIT = -77.675250;
// var latitudeRIT = 43.084132;
//
// const bounds = [
//     [-77.688972, 43.072019], // Southwest coordinates
//     [-77.663638, 43.092922] // Northeast coordinates
// ];
//
// const map = (window.map = new maplibregl.Map({
//     container: 'map',
//     zoom: 14.85,
//     center: [longitudeRIT, latitudeRIT],
//     pitch: 0,
//     hash: true,
//     style: {
//         version: 8,
//         sources: {
//             osm: {
//                 type: 'raster',
//                 tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
//                 tileSize: 256,
//                 attribution: '&copy; OpenStreetMap Contributors',
//                 maxzoom: 50
//             },
//             // Use a different source for terrain and hillshade layers, to improve render quality
//             terrainSource: {
//                 type: 'raster-dem',
//                 url: 'https://demotiles.maplibre.org/terrain-tiles/tiles.json',
//                 tileSize: 256
//             },
//             hillshadeSource: {
//                 type: 'raster-dem',
//                 url: 'https://demotiles.maplibre.org/terrain-tiles/tiles.json',
//                 tileSize: 256
//             }
//         },
//         layers: [
//             {
//                 id: 'osm',
//                 type: 'raster',
//                 source: 'osm'
//             },
//             {
//                 id: 'hills',
//                 type: 'hillshade',
//                 source: 'hillshadeSource',
//                 layout: {visibility: 'visible'},
//                 paint: {'hillshade-shadow-color': '#473B24'}
//             }
//         ],
//         terrain: {
//             source: 'terrainSource',
//             exaggeration: 1
//         }
//     },
//     maxZoom: 18,
//     maxPitch: 85,
//     maxBounds: bounds
// }));
//
// const geojson = {
//     'type': 'FeatureCollection',
//     'features': []
// };
//
// map.scrollZoom.disable();
// map.doubleClickZoom.disable();