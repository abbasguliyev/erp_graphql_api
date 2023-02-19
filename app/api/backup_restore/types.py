import graphene
from graphene import relay, InputObjectType
from graphene_django import DjangoObjectType
from backup_restore.models import BackupAndRestore

class BackupAndRestoreNode(DjangoObjectType):
    class Meta:
        model = BackupAndRestore
        interfaces = (relay.Node, )
        filter_fields = []