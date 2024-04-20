/// @file add_new_vehicle.js



function add_new_vehicle(lng, lat, heading) {

    const el = document.createElement('div');
    el.className = vehicleClassName;
    el.style.backgroundImage = `url(/car.png)`;
    el.style.width = `60px`;
    el.style.height = `60px`;
    el.style.backgroundRepeat = `no-repeat`;

    vehicle_markers.push(new maplibregl.Marker({element: el}).setLngLat([lng, lat]));
    vehicle_markers.at(0).addTo(map);
}
eel.expose(add_new_vehicle)