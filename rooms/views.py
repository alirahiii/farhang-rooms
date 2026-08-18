from django.http import HttpResponse


def home(request):
    return HttpResponse("سایت کار می‌کند")
