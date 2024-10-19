from permissions import choices, models


def create_permission_to_note_user_has_just_created(note, user):
    models.Permission.objects.create(user=user, type=choices.PermissionType.CREATOR, data=note)
