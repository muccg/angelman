from registry.groups.patient_registration.base import BaseRegistration
from rdrf.email_notification import process_notification
from rdrf.events import EventType
from registration.models import RegistrationProfile
from registry.patients.models import AddressType
from registry.patients.models import ClinicianOther
from registry.patients.models import ParentGuardian
from registry.patients.models import Patient
from registry.patients.models import PatientAddress
from registry.groups.models import WorkingGroup, CustomUser
from django.conf import settings


class AngelmanRegistration(BaseRegistration, object):

    def __init__(self, user, request):
        super(AngelmanRegistration, self).__init__(user, request)

    def process(self,):
        registry_code = self.request.POST['registry_code']
        registry = self._get_registry_object(registry_code)
        preferred_language = self.request.POST.get("preferred_language", "en")

        user = self._create_django_user(self.request, self.user, registry, is_parent=True)
        user.preferred_language = preferred_language

        try:
            clinician_id, working_group_id = self.request.POST['clinician'].split("_")
            clinician = CustomUser.objects.get(id=clinician_id)
            working_group = WorkingGroup.objects.get(id=working_group_id)
            user.working_groups = [working_group, ]
        except ValueError:
            clinician = None
            working_group, status = WorkingGroup.objects.get_or_create(
                name=self._UNALLOCATED_GROUP, registry=registry)
            user.working_groups = [working_group, ]

        user.save()

        patient = Patient.objects.create(
            consent=True,
            family_name=self.request.POST["surname"],
            given_names=self.request.POST["first_name"],
            date_of_birth=self.request.POST["date_of_birth"],
            sex=self.request.POST["gender"]
        )

        patient.rdrf_registry.add(registry.id)
        patient.working_groups.add(working_group.id)
        patient.clinician = clinician
        patient.home_phone = self.request.POST["phone_number"]
        patient.email = user.username
        patient.user = None

        patient.save()

        address = self._create_patient_address(patient, self.request)
        address.save()

        parent_guardian = self._create_parent(self.request)
        parent_guardian.patient.add(patient)
        parent_guardian.user = user
        parent_guardian.save()

        template_data = {
            "patient": patient,
            "parent": parent_guardian,
            "registration": RegistrationProfile.objects.get(user=user)
        }
        process_notification(registry_code, EventType.NEW_PATIENT, template_data)

        if "clinician-other" in self.request.POST['clinician']:
            other_clinician = ClinicianOther.objects.create(
                patient=patient,
                clinician_name=self.request.POST.get("other_clinician_name"),
                clinician_hospital=self.request.POST.get("other_clinician_hospital"),
                clinician_address=self.request.POST.get("other_clinician_address"),
                clinician_phone_number=self.request.POST.get("other_clinician_phone_number"),
                clinician_email=self.request.POST.get("other_clinician_email")
            )
            template_data = {
                "other_clinician": other_clinician,
                "patient": patient,
                "parent": parent_guardian
            }
            process_notification(
                registry_code, EventType.OTHER_CLINICIAN, template_data)

    def _create_parent(self, request):
        parent_guardian = ParentGuardian.objects.create(
            first_name=request.POST["parent_guardian_first_name"],
            last_name=request.POST["parent_guardian_last_name"],
            date_of_birth=request.POST["parent_guardian_date_of_birth"],
            gender=request.POST["parent_guardian_gender"],
            address=request.POST["parent_guardian_address"],
            suburb=request.POST["parent_guardian_suburb"],
            state=request.POST["parent_guardian_state"],
            postcode=request.POST["parent_guardian_postcode"],
            country=request.POST["parent_guardian_country"],
            phone=request.POST["parent_guardian_phone"],
        )
        return parent_guardian

    def _create_patient_address(self, patient, request, address_type="Postal"):
        same_address = "same_address" in request.POST

        address = PatientAddress.objects.create(
            patient=patient,
            address_type=self.get_address_type(address_type),
            address= request.POST["parent_guardian_address"] if same_address else request.POST["address"],
            suburb=request.POST["parent_guardian_suburb"] if same_address else request.POST["suburb"],
            state=request.POST["parent_guardian_state"] if same_address else request.POST["state"],
            postcode=request.POST["parent_guardian_postcode"] if same_address else request.POST["postcode"],
            country=request.POST["parent_guardian_country"] if same_address else request.POST["country"]
        )
        return address
