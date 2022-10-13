try:
    from django.urls import NoReverseMatch, resolve, reverse  # NOQA
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, resolve, reverse  # NOQA
