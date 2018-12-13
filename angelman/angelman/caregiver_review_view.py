import logging

from django.views.generic.base import View
from django.shortcuts import render
from registry.patients.models import ParentGuardian
from registry.patients.models import Patient
from registry.patients.models import PatientAddress
from registry.patients.models import ClinicianOther
from rdrf.models.definition.models import Registry
from rdrf.models.definition.models import ConsentQuestion
from rdrf.models.definition.models import CDEPermittedValueGroup

logger = logging.getLogger("registry_log")


CONSENT_SECTION_CODE = "ANGconsent"
CLINICIAN_CONSENT_CODE = "angconsent9"


def get_field(thing, field):
    if thing:
        return getattr(thing, field)
    else:
        return ""
    


class CaregiverReview:
    def __init__(self,
                 parent_model,
                 patient_model):

        # this whole page is specialised to Angelman
        self.registry_model = Registry.objects.get(code="ang")
        self.parent_model = parent_model
        self.patient_model = patient_model
        self.user = parent_model.user
        self.address = self._get_address()


    @property
    def street(self):
        return get_field(self.address, "address")

    @property
    def suburb(self):
        return get_field(self.address, "suburb")

    @property
    def postcode(self):
        return get_field(self.address, "postcode")

    def _get_address(self):
        addresses = [ addr for addr in PatientAddress.objects.filter(patient=self.patient_model)]
        if len(addresses) > 0:
            return addresses[0]
        

    def get_clinician_name(self):
        try:
            other_clinician = ClinicianOther.objects.get(patient=self.patient_model)
        except ClinicianOther.DoesNotExist:
            return None
        if other_clinician.user:
            name = "%s %s" % (other_clinician.user.first_name,
                              other_clinician.user.last_name)
            return name

    def get_clinician_consent(self):
        consent_model = ConsentQuestion.objects.get(code=CLINICIAN_CONSENT_CODE)
        return "checked" if self.patient_model.get_consent(consent_model) else ""

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
        parent_model = ParentGuardian.objects.get(user=request.user)
        patient_model = Patient.objects.get(id=patient_id)

        r = CaregiverReview(parent_model,
                            patient_model)
        

        context["r"] = r
        context['registry_code'] = registry_code
        context["parent"] = parent_model
        context['clinician_name'] = r.get_clinician_name()
        context['clinician_consent'] = r.get_clinician_consent()
        context["trials"] = r.get_trials()
        context["medical_problems"] = r.get_medical_problems()
        context["meds"] = r.get_meds()

        return render(request, "rdrf_cdes/caregiver_review.html", context)
