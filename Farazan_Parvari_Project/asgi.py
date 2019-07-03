import os
import os
import django
#from channels.asgi import get_channel_layer
from channels.routing import get_default_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Farazan_Parvari_Project.settings")
#channel_layer = get_channel_layer()
django.setup()
application = get_default_application()