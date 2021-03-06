# Generated by Django 4.0.2 on 2022-03-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('education', 'Education'), ('entertainment', 'Entertainment'), ('comics', 'Comics'), ('biography', 'Biography'), ('history', 'History'), ('novel', 'Novel'), ('fantasy', 'Fantasy'), ('thriller', 'Thriller'), ('romance', 'Romance'), ('scifi', 'Sci-Fi')], default='education', max_length=30),
        ),
        migrations.DeleteModel(
            name='category',
        ),
    ]
