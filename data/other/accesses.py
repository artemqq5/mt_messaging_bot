from enum import Enum


class TypeOfAdmins(Enum):
    ADMIN = "ADMIN"
    ADMIN_AGENCY = "ADMIN_AGENCY"
    ADMIN_APPS = "ADMIN_APPS"
    ADMIN_ACCOUNTS = "ADMIN_ACCOUNT"
    ADMIN_CREO = "ADMIN_CREO"
    ADMIN_PP = "ADMIN_PP"
    ADMIN_MEDIA = "ADMIN_MEDIA"


class TypeOfChats(Enum):
    AGENCY_FB = "agency_fb"
    AGENCY_GOOGLE = "agency_google"
    APPS = "apps"
    GOOGLE = "google"
    FB = "fb"
    CONSOLE = "console"
    CREO = "creo"
    PP_WEB = "pp_web"
    PP_ADS = "pp_ads"
    MEDIA = "media"
    ALL = "all"


def has_value_enum(enum, value):
    return value in (item.value for item in enum)


access_admin_to_chat = {
    TypeOfAdmins.ADMIN.value: [
        TypeOfChats.AGENCY_FB.value,
        TypeOfChats.AGENCY_GOOGLE.value,
        TypeOfChats.APPS.value,
        TypeOfChats.GOOGLE.value,
        TypeOfChats.FB.value,
        TypeOfChats.CONSOLE.value,
        TypeOfChats.CREO.value,
        TypeOfChats.PP_WEB.value,
        TypeOfChats.PP_ADS.value,
        TypeOfChats.MEDIA.value,
        TypeOfChats.ALL.value,
    ],

    TypeOfAdmins.ADMIN_AGENCY.value: [TypeOfChats.AGENCY_FB.value, TypeOfChats.AGENCY_GOOGLE.value],

    TypeOfAdmins.ADMIN_APPS.value: [TypeOfChats.APPS.value],

    TypeOfAdmins.ADMIN_ACCOUNTS.value: [
        TypeOfChats.GOOGLE.value,
        TypeOfChats.FB.value,
        TypeOfChats.CONSOLE.value
    ],

    TypeOfAdmins.ADMIN_CREO.value: [TypeOfChats.CREO.value],

    TypeOfAdmins.ADMIN_PP.value: [TypeOfChats.PP_WEB.value, TypeOfChats.PP_ADS.value],

    TypeOfAdmins.ADMIN_MEDIA.value: [TypeOfChats.MEDIA.value]
}
