# Generated by Django 4.2.8 on 2024-01-30 14:31
from django.db import migrations, models
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat


def migrate(apps, schema_editor):
    # I have to use the import here because i really need the class methods

    PivotMap = apps.get_model("pivots_manager", "PivotMap")
    Investigation = apps.get_model("investigations_manager", "Investigation")
    # I have to use the import here because i really need the class methods
    from api_app.models import Job as JobNonStoric

    last_root = JobNonStoric.objects.order_by("pk").filter(pivot_parent=None).first()
    if last_root:
        last_root.path = last_root._get_path(None, 1, 1)
        last_root.save()
        # all the other roots
        for job in (
            JobNonStoric.objects.exclude(pk=last_root.pk)
            .filter(pivot_parent=None)
            .iterator()
        ):
            newpath = last_root._inc_path()
            job.path = newpath
            job.save()
            last_root = job

    # we are now setting all the children
    for obj in PivotMap.objects.all().iterator():
        parent = obj.starting_job  # parent
        child = obj.ending_job
        parent.numchild += 1
        parent.save()
        child.depth = 2
        child.path = JobNonStoric._get_path(parent.path, child.depth, 1)
        child.save()
        if parent.numchild == 1:
            an = Investigation.objects.create(
                name="Pivot investigation",
                owner=parent.user,
                start_time=parent.received_request_time,
                end_time=child.finished_analysis_time,
                status="concluded",
            )
            an.jobs.add(parent)

    Investigation.objects.update(
        name=Concat(F("name"), Value(" #"), F("pk"), output_field=CharField())
    )


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0060_job_depth_job_numchild_job_path"),
        ("pivots_manager", "0025_alter_pivotmap_ending_job"),
        ("investigations_manager", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(migrate, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name="job",
                    name="path",
                    field=models.CharField(max_length=255, unique=True),
                ),
            ],
        )
    ]
