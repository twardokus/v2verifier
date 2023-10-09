/**
 * Clear all marker data.
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