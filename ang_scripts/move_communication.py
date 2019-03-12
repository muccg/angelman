from registry.patients.models import Patient
from rdrf.models.definition.models import ClinicalData
from rdrf.models.definition.models import Registry
import sys
import json
from datetime import datetime
from copy import deepcopy
from django.db import transaction
import django
django.setup()


OLD_FORM = "AngelmanRegistryBehaviourAndDevelopment"
NEW_FORM = "AngelmanRegistryCommunication"

SPEECH_SECTION = "ANGBEHDEVSPEECHLANGUAGE"
COMM_SECTION = "ANGBEHDEVCOMMUNICATION"
SECTIONS = [SPEECH_SECTION, COMM_SECTION]


class Logger:
    def __init__(self, patient):
        self.patient = patient
        self.pid = self.patient.id

    def log(self, msg, msg_type="INFO"):
        prefix = self.prefix()
        print("%s %s %s" % (prefix, msg_type, msg))

    def error(self, msg):
        self.log(msg, "ERROR")

    def warn(self, msg):
        self.log(msg, "WARN")

    def prefix(self):
        t = datetime.now()
        pid = self.patient.id
        return "%s pid %s:" % (t, pid)


def get_form(data, form_name):
    for form_dict in data["forms"]:
        if form_dict["name"] == form_name:
            return form_dict


def get_section(form_dict, section_code):
    if "sections" in form_dict:
        for section_dict in form_dict["sections"]:
            if section_dict["code"] == section_code:
                return section_dict


def form_exists(data, form_name):
    return len([f["name"] for f in data["forms"] if f["name"] == form_name]) == 1


def add_form(data, form_name):
    form_dict = {"name": form_name,
                 "sections": []}
    data["forms"].append(form_dict)
    return form_dict


class Munger:
    def __init__(self, registry, patient):
        self.registry = registry
        self.registry_code = registry.code
        self.patient = patient
        self.patient_id = patient.id
        self.context_id = None
        self.logger = Logger(patient)
        self.dry_run = True
        self.debug = True
        self.data = None
        self._load_data()

    def log(self, msg):
        self.logger.log(msg)

    def _load_data(self):
        self.data = self.patient.get_dynamic_data(self.registry)
        self.context_id = self.data["context_id"]

    def backup(self, data):
        filename = "patient_%s.json" % self.patient.id
        with open(filename, "w") as f:
            json.dump(data, f)

    def _print_data(self, msg):
        self.log(msg)
        if self.debug:
            self.log(str(self.data))

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def munge(self):
        self.log("starting to munge ...")
        self._print_data("data before munging:")
        if not self.data:
            self.logger.warn("no data - skipping")
            return

        if "forms" not in self.data:
            self.log("no forms key in data - skipping")
            return

        old_form = get_form(self.data, OLD_FORM)
        if not old_form:
            self.log("no %s form - skipping" % OLD_FORM)
            return

        backup_data = deepcopy(self.data)
        self.backup(backup_data)

        self._move_data(self.data, old_form, SPEECH_SECTION)
        self._move_data(self.data, old_form, COMM_SECTION)
        self._delete_old_sections(old_form)

        self._print_data("data after  munging:")
        self.save()

    def save(self):
        if not self.dry_run:
            self._save()
        else:
            self.log("dry run - not saving")

    def _save(self):
        self.log("really saving data ...")
        cd = self._get_clinical_data_model()
        cd.data = self.data
        cd.save()
        self.log("saved new data ok")

    def _get_clinical_data_model(self):
        collection = "cdes"
        return ClinicalData.objects.get(collection="cdes",
                                        registry_code=self.registry_code,
                                        django_model="Patient",
                                        django_id=self.patient_id,
                                        context_id=self.context_id)

    def _move_data(self, data, form_dict, section_code):
        section_dict = get_section(form_dict, section_code)
        section_copy = deepcopy(section_dict)
        if section_dict is None:
            self.logger.warn(
                "%s section does not exist - skipping" % section_code)
        else:
            if not form_exists(data, NEW_FORM):
                new_form = add_form(data, NEW_FORM)
                self.log("created form %s" % NEW_FORM)
            else:
                new_form = get_form(data, NEW_FORM)
                self.log("form %s already exists - using" % NEW_FORM)

            section_count = len(
                [s for s in new_form["sections"] if s["code"] == section_code])
            if section_count == 0:
                new_form["sections"].append(section_copy)
                self.log("added section %s to %s" % (section_code, NEW_FORM))
            else:
                self.error("section %s already exists in %s?" %
                           (section_code, NEW_FORM))

    def _delete_old_sections(self, old_form):
        old_form["sections"] = [
            s for s in old_form["sections"] if s["code"] not in SECTIONS]


def check_registry(reg):
    form_names = [f.name for f in ang.forms]
    if NEW_FORM not in form_names:
        raise Exception("registry not correct")
    if OLD_FORM not in form_names:
        raise Exception("registry not correct")

    section_codes = [s["code"] for f in reg.forms for s in f.section_models]
    if SPEECH_SECTION not in section_codes:
        raise Exception("registry not correct")


def run(dry_run=True):
    ang = Registry.objects.get(code="ang")
    check_registry(ang)
    backups = []

    for p in Patient.objects.all():
        m = Munger(ang, p)
        m.dry_run = dry_run
        m.munge()


if __name__ == '__main__':
    dry_run = False
    try:
        dry_run = sys.argv[1] != "real"
    except:
        pass

    if not dry_run:
        answer = input("NOT a dry run - Are you sure?")
        if answer not in ["Y", "y", "yes"]:
            sys.exit(0)

    try:
        with transaction.atomic():
            run(dry_run)
    except Exception as ex:
        print("run failed ! ( rolled back): %s" % ex)
