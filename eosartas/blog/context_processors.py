from .models import MenuItem

def menu_items(request):
    return {'menu_items': MenuItem.objects.all()}