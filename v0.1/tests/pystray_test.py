import pystray
from PIL import Image

# Define a callable function for setup
def setup(icon):
    print("Setup is being called")
    # Perform setup actions like defining a menu or loading resources
    icon.stop()

# Create an icon object with a placeholder image
icon = pystray.Icon('test_icon', Image.new('RGB', (64, 64), color='red'))

# Call run() with the setup function passed as the callable
icon.run(setup=setup)