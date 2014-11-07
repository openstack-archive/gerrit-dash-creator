#!/bin/sh

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

output_directory=doc/dashboards/

if [[ -e $output_directory ]]; then
    rm -f $output_directory/*
else
    mkdir -p $output_directory
fi

cp doc/source/conf.py $output_directory

echo "
html_theme_options = {
    'nosidebar': True
}" >> $output_directory/conf.py

for dashboard in $(find dashboards -name '*.dash' | sort); do
    output=$(basename $dashboard .dash)
    python gerrit_dash_creator/cmd/creator.py --template-directory templates \
    --template single.rst $dashboard > $output_directory/dashboard_$output.rst
done

echo "===========================
OpenStack Gerrit Dashboards
===========================

.. toctree::
" >> $output_directory/index.rst

for dashboard in $(find $output_directory -name 'dashboard_*.rst' | sort); do
    dashboard=$(basename $dashboard .rst)
    echo "  " $dashboard >> $output_directory/index.rst
done
