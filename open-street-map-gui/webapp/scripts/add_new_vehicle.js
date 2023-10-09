/**
 * Add a new vehicle to the GUI.
 *
 * @param {float} lng       longitude of the vehicle
 * @param {float} lat       latitude of the vehicle
 * @param {float} heading   heading of the vehicle
 *
 * @return {void}
 */
function add_new_vehicle(lng, lat, heading) {
    console.log(heading);
    geojson.features.push(
        {
            'type': 'Feature',
            'properties': {
                'message': '',
                'iconSize': [60, 60]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [lng, lat],
                'heading': heading
            },
            'image': {
                'path': `url(/car.png)`
            }
        }
    );
}
eel.expose(add_new_vehicle)