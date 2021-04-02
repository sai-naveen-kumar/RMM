from django.shortcuts import render
from . import systemconfig  

def index(request):
    print("Current View: Index View")
    config = systemconfig.Sysinfo()
    print(config)
    context = {'config' : config}
    return render(request, 'dashboard/index.html', context)
