from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tiempo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempo', models.IntegerField()),
                ('artista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.Artista')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musica.Usuario')),
            ],
        ),
    ]
