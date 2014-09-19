#!/usr/bin/python

import os
from six.moves import configparser
import sys

from launchpadlib import launchpad

from gerrit_dash_creator.cmd import creator

CACHE_DIR = os.path.expanduser('~/.cache/launchpadlib/')
SERVICE_ROOT = 'production'


def write_dash(project, bugs):
    config = configparser.ConfigParser()
    config.add_section('dashboard')
    config.set('dashboard', 'title',
               'Priortized Bug Fix Dashboard for %s' % project)
    config.set('dashboard', 'description', 'Bug Fix Inbox')
    config.set('dashboard', 'foreach', 'project:^openstack/%s ' % project)

    for milestone in bugs:
        for prio in bugs[milestone]:
            sec_name = 'section "%s - Importance:%s"' % (milestone, prio)
            config.add_section(sec_name)
            config.set(sec_name, 'query',
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


def main(args):
    try:
        project_name = args[1]
    except (ValueError, IndexError):
        print("Please specify a project.")
        return 1
    lpad = launchpad.Launchpad.login_anonymously(args[0], SERVICE_ROOT,
                                                 CACHE_DIR)
    project = lpad.projects[project_name]
    review_bugtasks = project.searchTasks(
        status=['In Progress'])

    bugs = {}
    for bug in review_bugtasks[:10]:
        milestone = pretty_milestone(bug.milestone)
        if milestone not in bugs:
            bugs[milestone] = {}
        if bug.importance not in bugs[milestone]:
            bugs[milestone][bug.importance] = []

        rev_no = review_id_from_bug(bug)
        if rev_no is not None:
            bugs[milestone][bug.importance].append(rev_no)
            print('[%s] %s -> %s' % (bug.importance,
                                     bug, rev_no))

    write_dash(project_name, bugs)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
