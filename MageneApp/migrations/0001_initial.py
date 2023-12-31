# Generated by Django 4.1.6 on 2023-02-19 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAM',
            fields=[
                ('CODEF', models.IntegerField(primary_key=True, serialize=False)),
                ('COMMUNEM', models.CharField(max_length=20, null=True)),
                ('DEPTM', models.CharField(max_length=20, null=True)),
                ('LIEUM', models.CharField(max_length=30, null=True)),
                ('DATEM', models.CharField(max_length=20, null=True)),
                ('CODESM', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='METIERS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LETTRE', models.CharField(max_length=1, null=True)),
                ('NOMPROF', models.CharField(max_length=20, null=True)),
                ('PERIODE', models.CharField(max_length=10, null=True)),
                ('OCCURENCE', models.IntegerField(null=True)),
                ('DEPT', models.CharField(max_length=20, null=True)),
                ('DEF', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SOURCES',
            fields=[
                ('CODES', models.IntegerField(primary_key=True, serialize=False)),
                ('TITRE', models.CharField(max_length=20, null=True)),
                ('DESCRIPTION', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='INDIV',
            fields=[
                ('CODEI', models.IntegerField(primary_key=True, serialize=False)),
                ('CODEPATRO', models.CharField(max_length=500, null=True)),
                ('COMMUNED', models.CharField(max_length=20, null=True)),
                ('COMMUNEN', models.CharField(max_length=20, null=True)),
                ('GENRE', models.CharField(max_length=1, null=True)),
                ('DEPTD', models.CharField(max_length=20, null=True)),
                ('DEPTN', models.CharField(max_length=20, null=True)),
                ('LIEUD', models.CharField(max_length=30, null=True)),
                ('LIEUN', models.CharField(max_length=30, null=True)),
                ('DATED', models.CharField(max_length=20, null=True)),
                ('DATEN', models.CharField(max_length=20, null=True)),
                ('NOM', models.CharField(max_length=20, null=True)),
                ('PRENOM', models.CharField(max_length=20, null=True)),
                ('PROF', models.CharField(max_length=30, null=True)),
                ('SIECLE', models.IntegerField(null=True)),
                ('CODESN', models.IntegerField(null=True)),
                ('CODESD', models.IntegerField(null=True)),
                ('CODEF', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MageneApp.fam')),
            ],
        ),
        migrations.AddField(
            model_name='fam',
            name='INDF',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FEMMELINK', to='MageneApp.indiv'),
        ),
        migrations.AddField(
            model_name='fam',
            name='INDM',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='HOMMELINK', to='MageneApp.indiv'),
        ),
    ]
