import django
django.setup()

from rdrf.models.definition.models import Registry
from rdrf.models.definition.models import RegistryForm

ang = Registry.objects.get(code="ang")

for form_model in ang.forms:
    if form_model.complete_form_cdes.all().count() > 0:
        print("resetting completion cdes on %s" % form_model.name)
        form_model.complete_form_cdes.set([])
        form_model.save()



