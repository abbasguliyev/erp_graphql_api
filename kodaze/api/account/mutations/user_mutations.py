import graphene
from api.account.types import (
    ChangePasswordInput,
    CreateGroupInput,
    CreateUserInput,
    GroupNode,
    ResetPasswordInput,
    UpdateGroupInput,
    UpdateUserInput,
    CustomUserNode
)

from django.contrib.auth import get_user_model
from company.models import Company, Department, Office, Position, Team
from account.models import EmployeeStatus
from django.contrib.auth.models import Group, Permission
from graphql import GraphQLError

from django_graphene_permissions import permissions_checker
from core.permissions import IsAdminUser
from api.account.permissions.user_permissions import (
    UserCreatePermissions,
    UserUpdatePermissions,
    UserDeletePermissions
)
User = get_user_model()

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(
            required=True, description="Fields required to create user"
        )

    user = graphene.Field(CustomUserNode)
    message = graphene.String()
    class Meta:
        description = "Create new User"
        model = User
    
    @permissions_checker([UserCreatePermissions])
    def mutate(root, info, input):
        try:
            company = Company.objects.get(id=input.get("company"))
        except:
            company = None
        try:
            office = Office.objects.get(id=input.get("office"))
        except:
            office = None
        try:
            department = Department.objects.get(id=input.get("department"))
        except:
            department = None
        try:
            position = Position.objects.get(id=input.get("position"))
        except:
            position = None
        try:
            team = Team.objects.get(id=input.get("team"))
        except:
            team = None
        try:
            employee_status = EmployeeStatus.objects.get(id=input.get("employee_status"))
        except:
            employee_status = None
        try:
            supervisor = User.objects.get(id=input.get("supervisor"))
        except:
            supervisor = None
        try:
            profile_image = info.context.FILES[input.get("profile_image")]
        except:
            profile_image = None
        try:
            photo_ID = info.context.FILES[input.get("photo_ID")]
        except:
            photo_ID = None
        try:
            back_photo_of_ID = info.context.FILES[input.get("back_photo_of_ID")]
        except:
            back_photo_of_ID = None
        try:
            driving_license_photo = info.context.FILES[input.get("driving_license_photo")]
        except:
            driving_license_photo = None
        user = User()
        user.first_name = input.get("first_name")
        user.last_name = input.get("last_name")
        user.username = input.get("username")
        user.email = input.get("email")
        user.date_of_birth = input.get("date_of_birth")
        user.start_date_of_work = input.get("start_date_of_work")
        user.dismissal_date = input.get("dismissal_date")
        user.phone_number_1 = input.get("phone_number_1")
        user.phone_number_2 = input.get("phone_number_2")
        user.profile_image = profile_image
        user.photo_ID = photo_ID
        user.back_photo_of_ID = back_photo_of_ID
        user.driving_license_photo = driving_license_photo
        user.company = company
        user.office = office
        user.department = department
        user.position = position
        user.team = team
        user.employee_status = employee_status
        user.salary_style = input.get("salary_style")
        user.contract_type = input.get("contract_type")
        user.salary = input.get("salary")
        user.note = input.get("note")
        user.supervisor = supervisor
        user.set_password(input.get("password")) 
        user.save()
        message = "User created"
        return CreateUser(user=user, message=message)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a user")
        input = UpdateUserInput(
            required=True, description="Fields required to Update User")

    user = graphene.Field(CustomUserNode)
    message = graphene.String()
    class Meta:
        description = "Update User"
        model = User

    @permissions_checker([UserUpdatePermissions])
    def mutate(root, info, input, id):
        User.objects.filter(pk=id).update(**input)
        user = User.objects.get(pk=id)
        message = "User updated"
        return UpdateUser(user=user, message=message)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a user")

    user = graphene.Field(CustomUserNode)
    message = graphene.String()

    class Meta:
        description = "Delete User"
        model = User
    
    @permissions_checker([UserDeletePermissions])
    def mutate(root, info, id):
        user = User.objects.get(pk=id)
        user.is_active = False
        user.save()
        message = "User deactivated"
        return DeleteUser(user=user, message=message)

class ChangePassword(graphene.Mutation):
    class Arguments:
        input = ChangePasswordInput(
            required=True,  description="Fields required to Create Group"
        )
    
    user = graphene.Field(CustomUserNode)
    message = graphene.String()
    
    class Meta:
        description = "Change password"
        model = User
        
    @permissions_checker([IsAdminUser])
    def mutate(root, info, input):
        user = User.objects.get(pk=info.context.user.id)
        if not user.check_password(input.get("old_password")):
            message = "Wrong Password"
            return GraphQLError(message)
        user.set_password(input.get("new_password"))
        user.save()
        message = "Password changed"
        return ChangePassword(user=user, message=message)
    
class ResetPassword(graphene.Mutation):
    class Arguments:
        input = ResetPasswordInput(
            required=True,  description="Fields required to Create Group"
        )
    
    user = graphene.Field(CustomUserNode)
    message = graphene.String()
    
    class Meta:
        description = "Reset password"
        model = User
        
    @permissions_checker([IsAdminUser])
    def mutate(root, info, input):
        user = User.objects.get(pk=input.get("username"))
        user.set_password(input.get("new_password"))
        user.save()
        message = "Password reseted"
        return ResetPassword(user=user, message=message)
    
class CreateGroup(graphene.Mutation):
    class Arguments:
        input = CreateGroupInput(
            required=True,  description="Fields required to Create Group"
        )
        
    group = graphene.Field(GroupNode)
    message = graphene.String()
    
    class Meta:
        description = "Create Group"
        model = Group
        
    @permissions_checker([IsAdminUser])
    def mutate(root, info, input):
        group = Group.objects.create(name=input.get("name"))
        for p in input.get("permissions"):
            perm = Permission.objects.filter(id=p).first()
            group.permissions.add(perm.id)
        group.save()
        message = "Group Created"
        return CreateGroup(group=group, message=message)
        
class UpdateGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a group")
        input = UpdateGroupInput(
            required=True,  description="Fields required to Update Group"
        )
        
    group = graphene.Field(GroupNode)
    message = graphene.String()
    
    class Meta:
        description = "Update Group"
        model = Group
        
    @permissions_checker([IsAdminUser])
    def mutate(root, info, id, input):
        Group.objects.filter(pk=id).update(**input)
        group = Group.objects.get(pk=id)
        message = "Group Updated"
        return UpdateGroup(group=group, message=message)
        
class DeleteGroup(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a group")
        
    message = graphene.String()
    
    class Meta:
        description = "Delete Group"
        model = Group
        
    @permissions_checker([IsAdminUser])
    def mutate(root, info, id):
        Group.objects.get(pk=id).delete()
        message = "Group Deleted"
        return DeleteGroup(message=message)