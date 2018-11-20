import logging
logger = logging.getLogger(__name__)

class ClinicanRegistrationError:
    pass

class ClinicianRegistration:
    def __init__(self, user, request):
        self.token = request.GET.get("token", None)
        self.user = user
        
    def process(self):
        registry_code = self.request.POST['registry_code']
        registry = self._get_registry_object(registry_code)
        preferred_language = self.request.POST.get("preferred_language", "en")

        user = self._create_django_user(self.request, self.user, registry, is_parent=True)
        user.preferred_language = preferred_language
        # Initially UNALLOCATED
        working_group, status = WorkingGroup.objects.get_or_create(name=self._UNALLOCATED_GROUP,
                                                                   registry=registry)

        user.working_groups = [working_group,]
        user.save()
        logger.debug("AngelmanRegistration process - created user")

        patient = Patient.objects.create(
            consent=True,
            family_name=self.request.POST["surname"],
            given_names=self.request.POST["first_name"],
            date_of_birth=self.request.POST["date_of_birth"],
            sex=self.request.POST["gender"]
        )

        patient.rdrf_registry.add(registry)
        patient.working_groups.add(working_group)
        patient.home_phone = self.request.POST["phone_number"]
        patient.email = user.username
        patient.user = None

        patient.save()
        logger.debug("AngelmanRegistration process - created patient")

        address = self._create_patient_address(patient, self.request)
        address.save()
        logger.debug("AngelmanRegistration process - created patient address")

        parent_guardian = self._create_parent(self.request)
        
        parent_guardian.patient.add(patient)
        parent_guardian.user = user
        parent_guardian.save()
        logger.debug("AngelmanRegistration process - created parent")

        template_data = {
            "patient": patient,
            "parent": parent_guardian,
            "registration": RegistrationProfile.objects.get(user=user)
        }

        process_notification(registry_code, EventType.NEW_PATIENT, template_data)
        logger.debug("AngelmanRegistration process - sent notification for NEW_PATIENT")




        
        from rdrf.models.workflow_models import ClinicianSignupRequest
        logger.debug("setting up clinician ..")
        try:
            csr = ClinicianSignupRequest.objects.get(token=self.token,
                                                     state="emailed")
                                                     
        except ClinicianSignupRequest.DoesNotExist:
            raise ClinicanRegistrationError("Unknown clinician")

        self.user.add_group("Clinical Staff")
        self.user.save()
