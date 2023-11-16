#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

"""
A tool to generate test matrix report for StackInsights Python Plugins
"""
import pkgutil

from stackinsights.plugins import __path__ as plugins_path

doc_head = """# Supported Libraries
This document is **automatically** generated from the StackInsights Python testing matrix.

The column of versions only indicates the set of library versions tested in a best-effort manner.

If you find newer major versions that are missing from the following table, and it's not documented as a limitation,
please PR to update the test matrix in the plugin.

Versions marked as NOT SUPPORTED may be due to
an incompatible version with Python in the original library
or a limitation of StackInsights auto-instrumentation (welcome to contribute!)

"""
table_head = """### Plugin Support Table
| Library | Python Version - Lib Version | Plugin Name |
| :--- | :--- | :--- |
"""


def generate_plugin_doc():
    """
    Generates a test matrix table to the current dir

    Returns: None

    """
    table_entries = []
    note_entries = []
    for importer, modname, _ispkg in pkgutil.iter_modules(plugins_path):
        plugin = importer.find_module(modname).load_module(modname)

        try:
            plugin_support_matrix = plugin.support_matrix  # type: dict
            plugin_support_links = plugin.link_vector  # type: list
            libs_tested = list(plugin_support_matrix.keys())
            links_tested = plugin_support_links  # type: list
            if plugin.note:
                note_entries.append(plugin.note)
        except AttributeError:
            raise AttributeError(f'Missing attribute in {modname}, please follow the correct plugin style.')

        for lib, link in zip(libs_tested, links_tested):  # NOTE: maybe a two lib support like http.server + werkzeug
            lib_entry = str(lib)
            lib_link = link
            version_vector = plugin_support_matrix[lib_entry]  # type: dict
            pretty_vector = ''
            for python_version in version_vector:  # e.g. {'>=3.10': ['2.5', '2.6'], '>=3.6': ['2.4.1', '2.5', '2.6']}
                lib_versions = version_vector[python_version]
                pretty_vector += f'Python {python_version} ' \
                                 f"- {str(lib_versions) if lib_versions else 'NOT SUPPORTED YET'}; "
            table_entry = f'| [{lib_entry}]({lib_link}) | {pretty_vector} | `{modname}` |'
            table_entries.append(table_entry)

    with open('docs/en/setup/Plugins.md', 'w') as plugin_doc:
        plugin_doc.write(doc_head)

        plugin_doc.write(table_head)
        for table_entry in table_entries:
            plugin_doc.write(f'{table_entry}\n')

        plugin_doc.write('### Notes\n')
        for note_entry in note_entries:
            plugin_doc.write(f'- {note_entry}\n')


if __name__ == '__main__':
    generate_plugin_doc()
