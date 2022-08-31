import graphene
from django_graphene_permissions import permissions_checker
from backup_restore.models import BackupAndRestore
from core.permissions import IsAdminUser
from django.core.management import call_command
import datetime
from graphql import GraphQLError


class Backup(graphene.Mutation):
    message = graphene.String()

    class Meta:
        description = "Create new Backup"
        model = BackupAndRestore

    @permissions_checker([IsAdminUser])
    def mutate(root, info):
        try:
            call_command("dbbackup")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.backup_date = f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    backup_date=f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            message = "Backup yerinə yetirildi"
            return Backup(message=message)
        except:
            message = "Error"
            raise GraphQLError(message=message)

class MediaBackup(graphene.Mutation):
    message = graphene.String()

    class Meta:
        description = "new Media Backup"
        model = BackupAndRestore

    @permissions_checker([IsAdminUser])
    def mutate(root, info):
        try:
            call_command("mediabackup", "--output-filename=media.zip")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.media_backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    media_backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            message = "Media Backup yerinə yetirildi"
            return Backup(message=message)
        except:
            message = "Error"
            raise GraphQLError(message=message)

class Restore(graphene.Mutation):
    message = graphene.String()

    class Meta:
        description = "new Restore"
        model = BackupAndRestore

    @permissions_checker([IsAdminUser])
    def mutate(root, info):
        try:
            call_command("dbrestore", "--noinput")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.restore_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    restore_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            message = "Restore yerinə yetirildi"
            return Backup(message=message)
        except:
            message = "Error"
            raise GraphQLError(message=message)
