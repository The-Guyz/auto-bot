from .models import *

def menu_links(request):
    links = User.objects.all()
    return dict(links=links)