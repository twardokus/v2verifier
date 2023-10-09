/**
 * Update all marker positions and rotations.
 *
 * @return {void}
 */
function update_markers() {
    geojson.features.forEach((marker) => {

        // create a DOM element for the marker
        const el = document.createElement('div');
        el.className = vehicleClassName;
        el.style.backgroundImage = `${marker.image.path}`;
        el.style.width = `${marker.properties.iconSize[0]}px`;
        el.style.height = `${marker.properties.iconSize[1]}px`;
        el.style.backgroundRepeat = `no-repeat`;
        console.log(marker.geometry.heading)
        // add marker to map
        new maplibregl.Marker({element: el})
            .setLngLat(marker.geometry.coordinates)
            .setRotation(marker.geometry.heading)
            .addTo(map);
    });
}
eel.expose(update_markers);