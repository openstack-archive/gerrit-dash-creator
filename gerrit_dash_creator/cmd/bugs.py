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


def print_dash_url(projects, bugs):
    config = configparser.ConfigParser()
    config.add_section('dashboard')
    config.set('dashboard', 'title',
               'Priortized Bug Fix Dashboard')
    config.set('dashboard', 'description', 'Bug Fix Inbox')

    proj_q = ['project:openstack/%s' % proj for proj in projects]
    config.set('dashboard', 'foreach',
               '(%s) status:open ' % ' OR '.join(proj_q))

    for label in bugs:
        for prio in bugs[label]:
            if len(bugs[label][prio]) == 0:
                continue
            sect = 'section "%s Importance %s"' % (label, prio)
            config.add_section(sect)
            config.set(sect, 'query',
                       ' OR '.join(['change:%s' % bug
                                    for bug in bugs[label][prio]]))

    print(creator.generate_dashboard_url(config))


def pretty_milestone(milestone_url):
    if milestone_url is None:
        return 'all'
    # https://api.launchpad.net/1.0/heat/+milestone/next:
    return str(milestone_url).split('/')[-1]


def review_id_from_bug(bug):
    reviews = set()
    reviews_merged = set()
    for msg in bug.bug.messages:
        if 'ix proposed' in msg.subject:
            for line in str(msg.content).split('\n'):
                if 'Review' in line:
                    reviews.add(line.split('/')[-1])
        if 'ix merged to' in msg.subject:
            for line in str(msg.content).split('\n'):
                if 'Reviewed: ' in line:
                    for rev in reviews:
                        if rev in line:
                            reviews_merged.add(rev)
    return (reviews - reviews_merged)


def get_options():
    """Parse command line arguments and options."""
    parser = argparse.ArgumentParser(
        description='Create a Gerrit dashboard URL from launchpad '
                    '"In Progress bugs')
    parser.add_argument('projects', nargs='+',
                        metavar='projects',
                        help='Launchpad Projects')
    parser.add_argument('--milestone', default=None,
                        help='Project Milestone')
    parser.add_argument('--tag', default=None,
                        help='Project Tag')
    return parser.parse_args()


def process_project(lp, opts, project_name, bugs):
    project = lp.projects[project_name]
    review_bugtasks = project.searchTasks(status=['In Progress'])

    for bug in review_bugtasks:
        importance = bug.importance
        milestone = pretty_milestone(bug.milestone)
        tags = bug.bug.tags

        label = None
        if opts.tag is not None:
            if opts.tag in tags:
                label = 'Tag:%s' % opts.tag

        if opts.milestone is not None:
            if milestone == opts.milestone:
                label = 'Milestone:%s' % milestone

        if label is None:
            continue

        if label not in bugs:
            bugs[label] = {}

        if importance not in bugs[label]:
            bugs[label][importance] = []

        for rev_no in review_id_from_bug(bug):
            bugs[label][importance].append(rev_no)
            print('[%s] %s -> %s' % (importance,
                                     bug, rev_no))


def main():
    """Entrypoint."""

    opts = get_options()
    lpad = launchpad.Launchpad.login_anonymously(sys.argv[0],
                                                 SERVICE_ROOT,
                                                 CACHE_DIR)
    bugs = {}
    for proj in opts.projects:
        process_project(lpad, opts, proj, bugs)

    print('')
    print_dash_url(opts.projects, bugs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
