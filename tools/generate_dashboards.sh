#!/bin/bash

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

set -x

OUTPUT_DIRECTORY=${OUTPUT_DIRECTORY:-doc/source/dashboards/}

if [[ -e $OUTPUT_DIRECTORY ]]; then
    rm -f $OUTPUT_DIRECTORY/*
else
    mkdir -p $OUTPUT_DIRECTORY
fi

for dashboard in $(find dashboards -name '*.dash' | sort); do
    output=$(basename $dashboard .dash)
    python gerrit_dash_creator/cmd/creator.py --template-directory templates \
    --template single.rst $dashboard > $OUTPUT_DIRECTORY/dashboard_$output.rst
done

echo "===========================
OpenStack Gerrit Dashboards
===========================

.. toctree::
   :maxdepth: 1
" >> $OUTPUT_DIRECTORY/index.rst

for dashboard in $(find $OUTPUT_DIRECTORY -name 'dashboard_*.rst' | sort); do
    dashboard=$(basename $dashboard .rst)
    echo "  " $dashboard >> $OUTPUT_DIRECTORY/index.rst
done
