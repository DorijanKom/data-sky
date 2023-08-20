from django.db import migrations, models
from django_celery_beat.models import IntervalSchedule, PeriodicTask

TEST_TASK_1 = {"name": "Test task 1", "task": "services.asyncq.core_tasks.test.test_1"}


###############################################################################
def add_test_tasks(apps, schema_editor):
    schedule = IntervalSchedule.objects.create(every=10, period=IntervalSchedule.SECONDS)
    PeriodicTask.objects.create(interval=schedule, **TEST_TASK_1)


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(db_index=True, max_length=254, unique=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_login_blocked", models.BooleanField(default=False)),
                ("is_blocked", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(add_test_tasks),
    ]
