import eel


eel.init(path='webapp',
         allowed_extensions=['.js', 'html', '.css'])



# Start the webapp (will open in Chrome/Chromium)
eel.start('osm-gui.html')