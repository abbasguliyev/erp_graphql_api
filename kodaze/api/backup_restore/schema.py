import graphene
from graphene_django.filter import DjangoFilterConnectionField

from api.backup_restore import mutations

from .resolvers import (
    resolve_backup_and_restore,
    resolve_backup_and_restores
)
from . types import BackupAndRestoreNode
from django_graphene_permissions import permissions_checker
from core.permissions import IsAdminUser


class BackupAndRestoreQuery(graphene.ObjectType):
    backup_and_restore = graphene.Field(
        BackupAndRestoreNode, description="Look up a backup and restore by ID",
        id=graphene.Argument(
            graphene.ID, description="ID for a backup and restore", required=True)
    )

    backup_and_restores = DjangoFilterConnectionField(
        BackupAndRestoreNode,
        description="List of backup and restores.",
    )

    @permissions_checker([IsAdminUser])
    def resolve_backup_and_restore(self, info, **data):
        id = data.get("id")
        return resolve_backup_and_restore(id)

    @permissions_checker([IsAdminUser])
    def resolve_backup_and_restores(self, info, **_kwargs):
        return resolve_backup_and_restores()

# ----------------------- Mutations ---------------------------------------


class BackupAndRestoreMutations(graphene.ObjectType):
    backup = mutations.Backup.Field()
    media_backup = mutations.MediaBackup.Field()
    restore = mutations.Restore.Field()
