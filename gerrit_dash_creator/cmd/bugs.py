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
import sys

from launchpadlib import launchpad
import six
from six.moves import configparser

from gerrit_dash_creator.cmd import creator

CACHE_DIR = os.path.expanduser('~/.cache/launchpadlib/')
SERVICE_ROOT = 'production'


def print_dash_url(opts, bugs):
    config = configparser.ConfigParser()
    config.add_section('dashboard')
    title = ','.join(opts.projects)
    if opts.milestone:
        title += ' milestone:%s' % opts.milestone
        if opts.tag:
            title += ' AND'
    if opts.tag:
        title += ' tag:%s' % opts.tag

    config.set('dashboard', 'title', title)
    config.set('dashboard', 'description', 'Bug Fix Inbox')

    proj_q = ['project:openstack/%s' % proj for proj in opts.projects]
    config.set('dashboard', 'foreach',
               '(%s) status:open ' % ' OR '.join(proj_q))

    for label in bugs:
        for prio in bugs[label]:
            if len(bugs[label][prio]) == 0:
                continue
            sect = 'section "%s Importance %s"' % (label, prio)
            if prio == 'None':
                sect = 'section "%s"' % label
            config.add_section(sect)
            config.set(sect, 'query',
                       ' OR '.join(['change:%s' % bug
                                    for bug in bugs[label][prio]]))

    print(creator.generate_dashboard_url(config))


def pretty_milestone(milestone_url):
    if milestone_url is None:
        return 'Unassigned'
    # https://api.launchpad.net/1.0/heat/+milestone/next:
    return str(milestone_url).split('/')[-1]


def review_id_from_bug(bug, project_name):
    reviews = set()
    reviews_ignored = set()
    for msg in bug.bug.messages:
        try:
            lines = six.text_type(msg.content).split('\n')
        except UnicodeEncodeError:
            print('non-ascii in bug %s' % bug.web_link)
            continue

        proposed = 'ix proposed to %s' % project_name
        merged = 'ix merged to %s' % project_name
        abandoned = 'Change abandoned on %s' % project_name
        if proposed in msg.subject:
            for line in lines:
                if 'Review: ' in line:
                    reviews.add(line.split('/')[-1])
        if merged in msg.subject or abandoned in msg.subject:
            for line in lines:
                if 'Review' in line:
                    reviews_ignored.add(line.split('/')[-1])
    live_reviews = (reviews - reviews_ignored)
    if len(live_reviews) == 0:
        print('bug %s has no reviews set to Triaged state' % bug.web_link)
    return live_reviews


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

    if opts.tag is None and opts.milestone is not None:
        from_milestone = project.getMilestone(name=opts.milestone)
        if not from_milestone:
            print('Origin milestone %s does not exist' %
                  opts.milestone)
            sys.exit(1)

        review_bugtasks = from_milestone.searchTasks(status=['In Progress'])
    else:
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

        if opts.tag is None and opts.milestone is None:
            # just place by milestone
            label = 'Milestone:%s' % milestone
            importance = 'None'

        if label is None:
            continue

        if label not in bugs:
            bugs[label] = {}

        if importance not in bugs[label]:
            bugs[label][importance] = []

        for rev_no in review_id_from_bug(bug, project_name):
            bugs[label][importance].append(rev_no)
            print('[%s] %s -> %s' % (importance,
                                     bug.web_link, rev_no))


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
    print_dash_url(opts, bugs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
