from enum import Enum


class TypeOfAdmins(Enum):
    ADMIN = "ADMIN"
    ADMIN_AGENCY = "ADMIN_AGENCY"
    ADMIN_APPS = "ADMIN_APPS"
    ADMIN_ACCOUNTS = "ADMIN_ACCOUNT"
    ADMIN_CREO = "ADMIN_CREO"
    ADMIN_PP = "ADMIN_PP"


class TypeOfChats(Enum):
    AGENCY = "AGENCY"
    APPS = "APPS"
    GOOGLE = "GOOGLE"
    FB = "FB"
    CONSOLE = "CONSOLE"
    CREO = "CREO"
    PP = "PP"


access_admin_to_chat = {
    TypeOfAdmins.ADMIN.name: [
        TypeOfChats.AGENCY.name,
        TypeOfChats.APPS.name,
        TypeOfChats.GOOGLE.name,
        TypeOfChats.FB.name,
        TypeOfChats.CONSOLE.name,
        TypeOfChats.CREO.name,
        TypeOfChats.PP.name
    ],

    TypeOfAdmins.ADMIN_AGENCY.name: [TypeOfChats.AGENCY.name],

    TypeOfAdmins.ADMIN_APPS.name: [TypeOfChats.APPS.name],

    TypeOfAdmins.ADMIN_ACCOUNTS.name: [
        TypeOfChats.GOOGLE.name,
        TypeOfChats.FB.name,
        TypeOfChats.CONSOLE.name
    ],

    TypeOfAdmins.ADMIN_CREO.name: [TypeOfChats.CREO.name],

    TypeOfAdmins.ADMIN_PP.name: [TypeOfChats.PP.name]
}
