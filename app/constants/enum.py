from enum import Enum


class ProjectPermission(str, Enum):
    VIEW = "VIEW"
    EDIT = "EDIT"
