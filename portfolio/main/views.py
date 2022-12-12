from django.views.generic import TemplateView, FormView
from . import decorators
from .forms import ContactForm, ContactEmail
from django.http import JsonResponse


# Create your views here.


class HomeView(FormView):
    template_name = "main/index.html"
    form_class = ContactForm

    @decorators.ajax_request
    def form_valid(self, form):
        email = ContactEmail(form)
        email.send_message()
        return JsonResponse({"message": "success"}, status=200)

    @decorators.ajax_request
    def form_invalid(self, form):
        return JsonResponse({'success': False,
                             'error': form.errors}, status=400)


class MiddleEarthProjectView(TemplateView):
    template_name = "main/middle_earth_project.html"


class PortfolioProjectView(TemplateView):
    template_name = "main/portfolio_project.html"
