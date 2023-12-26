from enum import Enum


class TypeOfAdmins(Enum):
    ADMIN = "ADMIN"
    ADMIN_AGENCY = "ADMIN_AGENCY"
    ADMIN_APPS = "ADMIN_APPS"
    ADMIN_ACCOUNTS = "ADMIN_ACCOUNT"


access_admin_to_chat = {
    TypeOfAdmins.ADMIN.name: ["AGENCY", "APPS", "GOOGLE", "FB", "CONSOLE"],
    TypeOfAdmins.ADMIN_AGENCY.name: ["AGENCY"],
    TypeOfAdmins.ADMIN_APPS.name: ["APPS"],
    TypeOfAdmins.ADMIN_ACCOUNTS.name: ["GOOGLE", "FB", "CONSOLE"]
}

