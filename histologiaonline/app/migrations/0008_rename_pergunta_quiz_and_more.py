# Generated by Django 4.2.7 on 2024-10-01 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_pergunta_resposta_tentativaquiz_delete_atividades'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pergunta',
            new_name='Quiz',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='resposta_correta',
            new_name='pergunta',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='texto',
            new_name='titulo',
        ),
        migrations.RenameField(
            model_name='resposta',
            old_name='pergunta',
            new_name='quiz',
        ),
        migrations.AddField(
            model_name='resposta',
            name='correta',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='resposta',
            name='ordem',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
