from django.shortcuts import render_to_response, RequestContext
from django.views.generic.base import View

class LandingView(View):

    def get(self, request):
        context = {}
        return render_to_response('rdrf_cdes/landing.html', context, context_instance=RequestContext(request))