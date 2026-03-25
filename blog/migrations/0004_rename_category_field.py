from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_blogpost_is_feature_alter_blogpost_excert"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpost",
            old_name="Category",
            new_name="category",
        ),
    ]
