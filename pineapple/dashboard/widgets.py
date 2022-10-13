from django import forms
from django.forms.widgets import Select, SelectMultiple


class DashboardSelect(Select):
    template_name = "dashboard/widgets/select.html"

    @property
    def media(self):
        return forms.Media(
            css={"all": ("vendor/select2/css/select2.min.css",)},
            js=("vendor/select2/js/select2.min.js",),
        )


class DashboardSelectMultiple(SelectMultiple):
    template_name = "dashboard/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs["multiple"] = "multiple"
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("vendor/select2/css/select2.min.css",)},
            js=("vendor/select2/js/select2.min.js",),
        )
