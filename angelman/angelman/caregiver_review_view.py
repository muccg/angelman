import logging

from django.views.generic.base import View
from django.shortcuts import render
from registry.patients.models import ParentGuardian
from registry.patients.models import Patient
from rdrf.models.definition.models import Registry
from rdrf.models.definition.models import CDEPermittedValueGroup




logger = logging.getLogger("registry_log")


class CaregiverReview:
    def __init__(self,
                  registry_model,
                  parent_model,
                  patient_model):
        self.registry_model = registry_model
        self.parent_model = parent_model
        self.patient_model = patient_model

    def get_clinician_name(self):
        return "Dr John Smith"

    def get_trials(self):
        return ["Trial 1", "Trial 2", "Trial 3"]

    def get_medical_problems(self):
        return ["Pneumonia/Respiratory",
                "Strep Throat",
                "Gastroesophageal Reflux",
                "Constipation",
                "Vomiting with Feeds",
                "Gagging",
                "Tight Heel Cords or Toe Walking",
                "Scoliosis",
                "Dental Problems",
                "Obesity",
                "Failure to Thrive",
                "Tube Feeding",
                "Eye Problems",
                "Hearing Problems"
                "Neurological Problems",
                "Auditory processing disorders",
                "Cortical myoclonus (tremors)",
                "Allergies",
                "Intolerances",
                "Other Medical Problems",
                ]


    def get_meds(self):
        return CDEPermittedValueGroup.objects.get(code="ANGMedIntListMaster").members(get_code=False)
    


class CaregiverReviewView(View):

  
    def get(self, request, registry_code, patient_id):
        context = {}
        registry_model = Registry.objects.get(code=registry_code)
        parent_model = ParentGuardian.objects.get(user=request.user)
        patient_model = Patient.objects.get(id=patient_id)

        r = CaregiverReview(registry_model,
                            parent_model,
                            patient_model)
        

        context['registry_code'] = registry_code
        context["parent"] = parent_model
        context['clinician_name'] = r.get_clinician_name()
        context["trials"] = r.get_trials()
        context["medical_problems"] = r.get_medical_problems()
        context["meds"] = r.get_meds()
        
        
       

        return render(request, "rdrf_cdes/caregiver_review.html", context)

   
