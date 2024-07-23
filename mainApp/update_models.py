from django.db import migrations

def set_default_value(apps, schema_editor):
    Product = apps.get_model('main', 'Product')
    Product.objects.filter(new_field=None).update(new_field='default_value')

class Migration(migrations.Migration):

    dependencies = [
        ('main', 'previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='new_field',
            field=models.CharField(default='default_value', max_length=100),
        ),
        migrations.RunPython(set_default_value),
    ]
