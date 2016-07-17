# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_auto_20160530_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientconsent',
            name='form',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/static/media/', location=b'/home/rodney/dev/angelman/rdrf/static/media'), upload_to=b'consents', null=True, verbose_name=b'Consent form', blank=True),
        ),
    ]
