from . import choices

permissions_relation = {
    choices.PermissionType.EDITOR: choices.PermissionType.READER,
    choices.PermissionType.READER: choices.PermissionType.EDITOR,
}
