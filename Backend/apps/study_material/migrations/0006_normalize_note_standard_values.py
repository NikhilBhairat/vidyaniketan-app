from django.db import migrations


def normalize_note_standards(apps, schema_editor):
    Note = apps.get_model('study_material', 'Note')

    mapping = {
        '5th': '5',
        '5th standard': '5',
        '5 standard': '5',
        '6th': '6',
        '6th standard': '6',
        '6 standard': '6',
        '7th': '7',
        '7th standard': '7',
        '7 standard': '7',
        '8th': '8',
        '8th standard': '8',
        '8 standard': '8',
        '9th': '9',
        '9th standard': '9',
        '9 standard': '9',
        '10th': '10',
        '10th standard': '10',
        '10 standard': '10',
    }

    for note in Note.objects.all().only('id', 'standard'):
        raw = (note.standard or '').strip()
        normalized = mapping.get(raw.lower())
        if normalized and normalized != note.standard:
            note.standard = normalized
            note.save(update_fields=['standard'])


class Migration(migrations.Migration):

    dependencies = [
        ('study_material', '0005_alter_note_standard_alter_note_student'),
    ]

    operations = [
        migrations.RunPython(normalize_note_standards, migrations.RunPython.noop),
    ]
