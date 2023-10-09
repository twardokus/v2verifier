/**
 * Clear all marker data for vehicles by removing the corresponding DOM objects. Also, reset
 * the length of the markers array (features) in the geojson data to zero.
 *
 * @return {void}
 */
function reset_markers() {
    geojson.features.length = 0;
    const vehicleElements = document.getElementsByClassName("vehicle");
    for(let i = vehicleElements.length - 1; i >= 0; --i) {
        vehicleElements[i].remove();
    }

}
eel.expose(reset_markers)