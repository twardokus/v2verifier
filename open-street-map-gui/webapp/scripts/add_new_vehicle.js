function add_new_vehicle(lng, lat, heading) {
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