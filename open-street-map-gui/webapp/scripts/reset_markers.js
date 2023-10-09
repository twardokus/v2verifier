function reset_markers() {
    geojson.features.length = 0;
}
eel.expose(reset_markers)