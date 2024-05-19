/**
 * Clear all marker data for vehicles by removing the corresponding DOM objects. Also, reset
 * the length of the markers array (features) in the geojson data to zero.
 *
 * @return {void}
 */

function reset_markers() {
    vehicle_markers.forEach((marker) => {
        marker.remove();
    });
    vehicle_markers = [];
}
eel.expose(reset_markers)