import logging
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404


class ReviewView(View):
    def get(self, request, token):
        registry_model, patient_model = self.get_models_from_token(token)
        template = self.get_template()


    def get_template(self):
        raise Exception("subclass responsibility")


    def post(self, request):
        token = self._get_token(request)
        data = self.get_reviewed_data(token)

        if self.data_valid(data):
            try:
                with transaction.atomic():
                    self.update_data(
    
    
        
