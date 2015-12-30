#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os
import os.path
import sys

import jinja2
import six
from six.moves import configparser
from six.moves.urllib import parse as urllib_parse


def escape(buff):
    """Because otherwise Firefox is a sad panda."""
    return buff.replace(',', '%2c').replace('-', '%2D')


def generate_dashboard_url(dashboard):
    """Generate a dashboard URL from a given definition."""
    try:
        title = dashboard.get('dashboard', 'title')
    except configparser.NoOptionError:
        raise ValueError("option 'title' in section 'dashboard' not set")

    try:
        foreach = dashboard.get('dashboard', 'foreach')
    except configparser.NoOptionError:
        raise ValueError("option 'foreach' in section 'dashboard' not set")

    try:
        baseurl = dashboard.get('dashboard', 'baseurl')
    except configparser.NoOptionError:
        baseurl = 'https://review.openstack.org/#/dashboard/?'

    url = baseurl
    url += escape(urllib_parse.urlencode({'title': title,
                                          'foreach': foreach}))
    for section in dashboard.sections():
        if not section.startswith('section'):
            continue

        try:
            query = dashboard.get(section, 'query')
        except configparser.NoOptionError:
            raise ValueError("option 'query' in '%s' not set" % section)

        title = section[9:-1]
        encoded = escape(urllib_parse.urlencode({title: query}))
        url += "&%s" % encoded
    return url


def get_options():
    """Parse command line arguments and options."""
    parser = argparse.ArgumentParser(
        description='Create a Gerrit dashboard URL from specified dashboard '
                    'definition files')
    parser.add_argument('dashboard_paths', nargs='+',
                        metavar='dashboard_path',
                        help='Path to a dashboard definition file or a '
                             'directory containing a set of dashboard '
                             'definition files with the file suffix .dash.')
    parser.add_argument('--check-only', default=False, action="store_true",
                        help='Only check the syntax of the specified '
                             'dasbhoard files')
    parser.add_argument('--template', default='single.txt',
                        help='Name of template')
    parser.add_argument('--template-directory',
                        default="templates",
                        help='Directory to scan for template files')
    parser.add_argument('--template-file', default=None,
                        help='Location of a specific template file')
    return parser.parse_args()


def read_dashboard_file(dashboard_file):
    """Read and parse a dashboard definition from a specified file."""
    if (not os.path.isfile(dashboard_file) or
            not os.access(dashboard_file, os.R_OK)):
        raise ValueError("dashboard file '%s' is missing or "
                         "is not readable" % dashboard_file)
    dashboard = configparser.ConfigParser()
    dashboard.readfp(open(dashboard_file))
    return dashboard


def load_template(template_file=None, template_directory=None,
                  template_name=None):
    """Load the specified template."""
    if template_file:
        template_name = os.path.basename(template_file)
        template_directory = os.path.dirname(os.path.abspath(template_file))

    try:
        loader = jinja2.FileSystemLoader(template_directory)
        environment = jinja2.Environment(loader=loader)
        template = environment.get_template(template_name)
    except (jinja2.exceptions.TemplateError, IOError) as e:
        print("error: opening template '%s' failed: %s" %
              (template_name, e.__class__.__name__))
        return

    return template


def get_configuration(dashboard):
    """Returns the configuration of a dashboard as string."""
    configuration = six.StringIO()
    dashboard.write(configuration)
    result = configuration.getvalue()
    configuration.close()
    return result


def generate_dashboard_urls(dashboards, template):
    """Prints the dashboard URLs of a set of dashboards."""
    result = 0

    for dashboard_file in dashboards:
        dashboard = dashboards[dashboard_file]
        try:
            url = generate_dashboard_url(dashboard)
        except ValueError as e:
            raise ValueError("generating dashboard '%s' failed: %s" %
                             (dashboard_file, e))
            result = 1
            continue

        variables = {
            'url': url,
            'title': dashboard.get('dashboard', 'title') or None,
            'description': dashboard.get('dashboard', 'description') or None,
            'configuration': get_configuration(dashboard)
        }
        print(template.render(variables))

    return result


def load_dashboards(paths):
    """Load specified dashboards from files or directories."""
    dashboards = {}
    for dashboard_path in paths:
        dashboard_files = []
        if os.path.isdir(dashboard_path):
            for root, dirs, files in os.walk(dashboard_path):
                for file in files:
                    if file.endswith('.dash'):
                        dashboard_files.append(os.path.join(root, file))
        else:
            dashboard_files.append(dashboard_path)

        for dashboard_file in dashboard_files:
            try:
                dashboards[dashboard_file] = read_dashboard_file(
                    dashboard_file
                )
            except configparser.Error as e:
                raise ValueError("dashboard file '%s' cannot be "
                                 "parsed: %s" % (dashboard_file, e))

    return dashboards


def main():
    """Entrypoint."""
    opts = get_options()

    template = None
    if not opts.check_only:
        template = load_template(
            template_file=opts.template_file,
            template_directory=opts.template_directory,
            template_name=opts.template
        )

    try:
        dashboards = load_dashboards(opts.dashboard_paths)
        if not opts.check_only and template:
            generate_dashboard_urls(dashboards, template)
        elif not opts.check_only and not template:
            return 1
    except ValueError as e:
        print("error: %s" % e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
