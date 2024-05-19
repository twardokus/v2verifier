/**
 * Update all marker positions and rotations.
 *
 * @return {void}
 */
function add_vehicle_markers_to_map() {
    vehicle_markers.forEach((marker) => {
        marker.addTo(map);
    });
}
eel.expose(add_vehicle_markers_to_map);