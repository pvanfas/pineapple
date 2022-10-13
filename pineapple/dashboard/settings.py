import copy
import logging
from typing import Any

from django.conf import settings

from .utils import get_admin_url, get_model_meta

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: dict[str, Any] = {
    # title of the window (Will default to current_admin_site.site_title)
    "site_title": None,
    # Title on the login screen (19 chars max) (will default to current_admin_site.site_header)
    "site_header": None,
    # Title on the brand (19 chars max) (will default to current_admin_site.site_header)
    "site_brand": None,
    # Relative path to logo for your site, used for brand on top left (must be present in static files)
    "site_logo": "dashboard/img/logo.svg",
    # CSS classes that are applied to the logo
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome",
    # Copyright on the footer
    "copyright": "",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": None,
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the nav bar
    "topmenu_links": [],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    "usermenu_links": [],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_with_respect_to": [],
    # Custom links to append to side menu app groups, keyed on app name
    "custom_links": {},
    # Custom icons for side menu apps/models See the link below
    # https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,
    # 5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fa fa-volleyball-ball",
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    "related_modal_active": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

#######################################
# Currently available UI tweaks       #
# Use the UI builder to generate this #
#######################################

DEFAULT_UI_TWEAKS: dict[str, Any] = {
    # Small text on the top navbar
    "navbar_small_text": False,
    # Small text on the footer
    "footer_small_text": False,
    # Small text everywhere
    "body_small_text": False,
    # Small text on the brand/logo
    "brand_small_text": False,
    # brand/logo background colour
    "brand_colour": False,
    # Link colour
    "accent": "accent-primary",
    # topmenu colour
    "navbar": "navbar-light",
    # topmenu border
    "no_navbar_border": False,
    # Make the top navbar sticky, keeping it in view as you scroll
    "navbar_fixed": True,
    # Whether to constrain the page to a box (leaving big margins at the side)
    "layout_boxed": False,
    # Make the footer sticky, keeping it in view all the time
    "footer_fixed": False,
    # Make the sidebar sticky, keeping it in view as you scroll
    "sidebar_fixed": True,
    # sidemenu colour
    "sidebar": "",
    # sidemenu small text
    "sidebar_nav_small_text": False,
    # Disable expanding on hover of collapsed sidebar
    "sidebar_disable_expand": False,
    # Indent child menu items on sidebar
    "sidebar_nav_child_indent": False,
    # Use a compact sidebar
    "sidebar_nav_compact_style": False,
    # Use the AdminLTE2 style sidebar
    "sidebar_nav_legacy_style": False,
    # Use a flat style sidebar
    "sidebar_nav_flat_style": False,
    # Bootstrap theme to use (default, or from bootswatch, see THEMES below)
    "theme": "default",
    # Theme to use instead if the user has opted for dark mode (e.g darkly/cyborg/slate/solar/superhero)
    "dark_mode_theme": None,
    # The classes/styles to use with buttons
    "button_classes": {
        "primary": "btn-sm btn-outline-primary",
        "secondary": "btn-sm btn-outline-secondary",
        "info": "btn-sm btn-outline-info",
        "warning": "btn-sm btn-outline-warning",
        "danger": "btn-sm btn-outline-danger",
        "success": "btn-sm btn-outline-success",
    },
}

CHANGEFORM_TEMPLATES = {
    "single": "dashboard/includes/single.html",
    "carousel": "dashboard/includes/carousel.html",
    "collapsible": "dashboard/includes/collapsible.html",
    "horizontal_tabs": "dashboard/includes/horizontal_tabs.html",
    "vertical_tabs": "dashboard/includes/vertical_tabs.html",
}


def get_search_model_string(dashboard_settings: dict) -> str:
    """
    Get a search model string for reversing an admin url.

    Ensure the model name is lower cased but remain the app name untouched.
    """

    app, model_name = dashboard_settings["search_model"].split(".")
    return f"{app}.{model_name.lower()}"


def get_settings() -> dict:
    dashboard_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {
        x: y
        for x, y in getattr(settings, "DASHBOARD_SETTINGS", {}).items()
        if y is not None
    }
    dashboard_settings.update(user_settings)

    # Extract search url from search model
    if dashboard_settings["search_model"]:
        dashboard_settings["search_url"] = get_admin_url(
            get_search_model_string(dashboard_settings)
        )
        model_meta = get_model_meta(dashboard_settings["search_model"])
        if model_meta:
            dashboard_settings["search_name"] = model_meta.verbose_name_plural.title()
        else:
            dashboard_settings["search_name"] = (
                dashboard_settings["search_model"].split(".")[-1] + "s"
            )

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if type(dashboard_settings["hide_apps"]) == str:
        dashboard_settings["hide_apps"] = [dashboard_settings["hide_apps"]]
    dashboard_settings["hide_apps"] = [
        x.lower() for x in dashboard_settings["hide_apps"]
    ]

    if type(dashboard_settings["hide_models"]) == str:
        dashboard_settings["hide_models"] = [dashboard_settings["hide_models"]]
    dashboard_settings["hide_models"] = [
        x.lower() for x in dashboard_settings["hide_models"]
    ]

    # Ensure icon model names and classes are lower case
    dashboard_settings["icons"] = {
        x.lower(): y.lower() for x, y in dashboard_settings.get("icons", {}).items()
    }

    # Default the site icon using the site logo
    dashboard_settings["site_icon"] = (
        dashboard_settings["site_icon"] or dashboard_settings["site_logo"]
    )

    # ensure all model names are lower cased
    dashboard_settings["changeform_format_overrides"] = {
        x.lower(): y.lower()
        for x, y in dashboard_settings.get("changeform_format_overrides", {}).items()
    }
    return dashboard_settings


def get_ui_tweaks() -> dict:
    raw_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    raw_tweaks.update(getattr(settings, "DASHBOARD_UI_TWEAKS", {}))
    tweaks = {x: y for x, y in raw_tweaks.items() if y not in (None, "", False)}

    # These options dont work well together
    if tweaks.get("layout_boxed"):
        tweaks.pop("navbar_fixed", None)
        tweaks.pop("footer_fixed", None)

    bool_map = {
        "navbar_small_text": "text-sm",
        "footer_small_text": "text-sm",
        "body_small_text": "text-sm",
        "brand_small_text": "text-sm",
        "sidebar_nav_small_text": "text-sm",
        "no_navbar_border": "border-bottom-0",
        "sidebar_disable_expand": "sidebar-no-expand",
        "sidebar_nav_child_indent": "nav-child-indent",
        "sidebar_nav_compact_style": "nav-compact",
        "sidebar_nav_legacy_style": "nav-legacy",
        "sidebar_nav_flat_style": "nav-flat",
        "layout_boxed": "layout-boxed",
        "sidebar_fixed": "layout-fixed",
        "navbar_fixed": "layout-navbar-fixed",
        "footer_fixed": "layout-footer-fixed",
        "actions_sticky_top": "sticky-top",
    }

    for key, value in bool_map.items():
        if key in tweaks:
            tweaks[key] = value

    def classes(*args: str) -> str:
        return " ".join([tweaks.get(arg, "") for arg in args]).strip()

    ret = {
        "raw": raw_tweaks,
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent",
            "body_small_text",
            "navbar_fixed",
            "footer_fixed",
            "sidebar_fixed",
            "layout_boxed",
        ),
        "actions_classes": classes("actions_sticky_top"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
        "button_classes": tweaks["button_classes"],
    }
    return ret
