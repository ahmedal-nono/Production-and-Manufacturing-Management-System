# Safe text -> FK conversion for Workstation.work_center.
# 0001 created work_center as an FK, 0003 downgraded it to TextField and the
# legacy values are work-center *names*. This migration adds a temporary FK
# column, copies the legacy values into it (by id, then by name), drops the
# text column and renames the FK into place.

import django.db.models.deletion
from django.db import migrations, models


def text_to_fk(apps, schema_editor):
    Workstation = apps.get_model('workcentre', 'Workstation')
    WorkCenter = apps.get_model('workcentre', 'WorkCenter')

    centers = {c.pk: c for c in WorkCenter.objects.all()}
    by_name = {c.name.strip().lower(): c.pk for c in centers.values()}

    for ws in Workstation.objects.all():
        raw = getattr(ws, 'work_center', None)  # legacy text value
        target_id = None
        if raw:
            raw = str(raw).strip()
            if raw.isdigit() and int(raw) in centers:
                target_id = int(raw)
            else:
                target_id = by_name.get(raw.lower())
        ws.work_center_ref_id = target_id
        ws.save(update_fields=['work_center_ref'])


def fk_to_text(apps, schema_editor):
    Workstation = apps.get_model('workcentre', 'Workstation')
    WorkCenter = apps.get_model('workcentre', 'WorkCenter')
    names = dict(WorkCenter.objects.values_list('pk', 'name'))

    for ws in Workstation.objects.all():
        ws.work_center = names.get(ws.work_center_ref_id)
        ws.save(update_fields=['work_center'])


class Migration(migrations.Migration):

    dependencies = [
        ('workcentre', '0004_alter_workstation_machines_alter_workstation_tools'),
    ]

    operations = [
        migrations.AddField(
            model_name='workstation',
            name='work_center_ref',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='workcentre.workcenter',
            ),
        ),
        migrations.RunPython(text_to_fk, fk_to_text),
        migrations.RemoveField(
            model_name='workstation',
            name='work_center',
        ),
        migrations.RenameField(
            model_name='workstation',
            old_name='work_center_ref',
            new_name='work_center',
        ),
    ]
