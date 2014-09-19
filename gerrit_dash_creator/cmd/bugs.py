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
from six.moves import configparser
import sys

from launchpadlib import launchpad

from gerrit_dash_creator.cmd import creator

CACHE_DIR = os.path.expanduser('~/.cache/launchpadlib/')
SERVICE_ROOT = 'production'


def print_dash_url(project, bugs):
    config = configparser.ConfigParser()
    config.add_section('dashboard')
    config.set('dashboard', 'title',
               'Priortized Bug Fix Dashboard for %s' % project)
    config.set('dashboard', 'description', 'Bug Fix Inbox')
    config.set('dashboard', 'foreach',
               'project:^openstack/%s status:open NOT owner:self' % project)

    for milestone in bugs:
        for prio in bugs[milestone]:
            sect = 'section "Milestone %s Importance %s"' % (milestone, prio)
            config.add_section(sect)
            config.set(sect, 'query',
                       ' OR '.join(['change:%s' % bug
                                    for bug in bugs[milestone][prio]]))

    print(creator.generate_dashboard_url(config))


def pretty_milestone(milestone_url):
    if milestone_url is None:
        return 'None'
    # https://api.launchpad.net/1.0/heat/+milestone/next:
    return str(milestone_url).split('/')[-1]


def review_id_from_bug(bug):
    for msg in bug.bug.messages:
        if 'Fix proposed' in msg.subject:
            for line in str(msg.content).split('\n'):
                if 'Review' in line:
                    return line.split('/')[-1]


def get_options():
    """Parse command line arguments and options."""
    parser = argparse.ArgumentParser(
        description='Create a Gerrit dashboard URL from launchpad '
                    '"In Progress bugs')
    parser.add_argument('milestones', nargs='+',
                        metavar='milestones',
                        help='Allowed milestones')
    parser.add_argument('--project', default=None,
                        help='Launchpad project')
    return parser.parse_args()


def main():
    """Entrypoint."""

    opts = get_options()
    lpad = launchpad.Launchpad.login_anonymously(sys.argv[0],
                                                 SERVICE_ROOT,
                                                 CACHE_DIR)
    project = lpad.projects[opts.project]
    review_bugtasks = project.searchTasks(status=['In Progress'])

    bugs = {}
    for bug in review_bugtasks:
        milestone = pretty_milestone(bug.milestone)
        if milestone not in opts.milestones:
            continue
        if milestone not in bugs:
            bugs[milestone] = {}

        if bug.importance not in bugs[milestone]:
            bugs[milestone][bug.importance] = []

        rev_no = review_id_from_bug(bug)
        if rev_no is not None:
            bugs[milestone][bug.importance].append(rev_no)
            print('[%s] %s -> %s' % (bug.importance,
                                     bug, rev_no))

    print('')
    print_dash_url(opts.project, bugs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
