from .models import MenuItem

def menu_items(request):
    info = {'ADDRESS': 'Αμβρακίας 38',
            'DAYS': 'Δευτέρα -Τετάρτη - Παρασκευή',
            'HOURS': '9-10μμ',
            'EMAIL': 'eosartas1988@gmail.com',
            'TELEPHONE': '26810 28030'
            }
    return {'menu_items': MenuItem.objects.all(),
            'info': info
            }