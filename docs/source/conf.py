# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import inspect
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fby_market.settings')
django.setup()

# Django sphinx setup by https://gist.github.com/codingjoe/314bda5a07ff3b41f247

# Stop Django from executing DB queries
from django.db.models.query import QuerySet

QuerySet.__repr__ = lambda self: self.__class__.__name__

try:
    import enchant  # NoQA
except ImportError:
    enchant = None


def process_django_models(app, what, name, obj, options, lines):
    """Append params from fields to model documentation."""
    from django.utils.encoding import force_text
    from django.utils.html import strip_tags
    from django.db import models

    spelling_white_list = ['', '.. spelling::']

    if inspect.isclass(obj) and issubclass(obj, models.Model):
        for field in obj._meta.fields:
            help_text = strip_tags(force_text(field.help_text))
            verbose_name = force_text(field.verbose_name).capitalize()

            if help_text:
                lines.append(':param %s: %s - %s' % (field.attname, verbose_name, help_text))
            else:
                lines.append(':param %s: %s' % (field.attname, verbose_name))

            if enchant is not None:
                from enchant.tokenize import basic_tokenize

                words = verbose_name.replace('-', '.').replace('_', '.').split('.')
                words = [s for s in words if s != '']
                for word in words:
                    spelling_white_list += ["    %s" % ''.join(i for i in word if not i.isdigit())]
                    spelling_white_list += ["    %s" % w[0] for w in basic_tokenize(word)]

            field_type = type(field)
            module = field_type.__module__
            if 'django.db.models_addon' in module:
                # scope with django.db.models_addon * imports
                module = 'django.db.models_addon'
            lines.append(':type %s: %s.%s' % (field.attname, module, field_type.__name__))
        if enchant is not None:
            lines += spelling_white_list
    return lines


def process_modules(app, what, name, obj, options, lines):
    """Add module names to spelling white list."""
    if what != 'module':
        return lines
    from enchant.tokenize import basic_tokenize

    spelling_white_list = ['', '.. spelling::']
    words = name.replace('-', '.').replace('_', '.').split('.')
    words = [s for s in words if s != '']
    for word in words:
        spelling_white_list += ["    %s" % ''.join(i for i in word if not i.isdigit())]
        spelling_white_list += ["    %s" % w[0] for w in basic_tokenize(word)]
    lines += spelling_white_list
    return lines


def skip_queryset(app, what, name, obj, skip, options):
    """Skip queryset subclasses to avoid database queries."""
    from django.db import models
    if isinstance(obj, (models.QuerySet, models.manager.BaseManager)) or name.endswith('objects'):
        return True
    return skip


def setup(app):
    # Register the docstring processor with sphinx
    app.connect('autodoc-process-docstring', process_django_models)
    app.connect('autodoc-skip-member', skip_queryset)
    if enchant is not None:
        app.connect('autodoc-process-docstring', process_modules)
    app.add_css_file('theme_wide.css')


# -- Project information -----------------------------------------------------

project = 'FBY Market Provider'
copyright = '2021, SHP, s101, group 01'
author = 'SHP, s101, group 01'

# The full version, including alpha/beta/rc tags
release = '0.0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.inheritance_diagram',
    'sphinx_rtd_theme',
]

if enchant is not None:
    extensions.append('sphinxcontrib.spelling')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'ru'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
import sphinx_redactor_theme
html_theme = 'sphinx_redactor_theme'
html_theme_path = [sphinx_redactor_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'django': ('https://docs.djangoproject.com/en/3.1/', 'https://docs.djangoproject.com/en/3.1/_objects/'),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


coverage_show_missing_items = True


# spell checking
spelling_lang = 'ru_RU'
# spelling_word_list_filename = 'spelling_wordlist.txt'
spelling_show_suggestions = True
spelling_ignore_pypi_package_names = True
