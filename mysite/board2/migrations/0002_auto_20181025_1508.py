# Generated by Django 2.0.7 on 2018-10-25 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board2', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['post', 'display', 'list_order']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['post_class', 'display', 'list_order']},
        ),
        migrations.AddField(
            model_name='comment',
            name='display',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1),
        ),
        migrations.AddField(
            model_name='comment',
            name='original_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='original_cmnt', to='board2.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='display',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1),
        ),
        migrations.AddField(
            model_name='post',
            name='how_many_replied',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='upload',
            field=models.FileField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='list_order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='board2.Post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_to', to='board2.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='writer',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='writer',
            field=models.CharField(max_length=20),
        ),
    ]
