from backup_restore.models import BackupAndRestore


def resolve_backup_and_restore(id):
    return BackupAndRestore.objects.filter(pk=id).first()


def resolve_backup_and_restores():
    return BackupAndRestore.objects.all()
