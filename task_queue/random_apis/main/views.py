from django.shortcuts import render
from django.views import View
from .celery_task import send_tasks


# Create your views here.

class APIView(View):

    @staticmethod
    def get(request):
        return render(request, 'main/random_apis.html', context={"api": False})

    @staticmethod
    def post(request):
        api_results = send_tasks()
        return render(request, 'main/random_apis.html', context={"api": api_results})
