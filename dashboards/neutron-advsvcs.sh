[dashboard]
title = Neutron Advanced Services Review Inbox (master branch only)
description = Review Inbox
foreach = (project:openstack/neutron-lbaas OR project:openstack/neutron-fwaas OR project:openstack/neutron-vpnaas) status:open NOT owner:self NOT label:Workflow<=-1 label:Verified>=1,jenkins NOT label:Code-Review>=-2,self branch:master

[section "Needs Feedback (Changes older than 5 days that have not been reviewed by anyone)"]
query = NOT label:Code-Review<=2 age:5d

[section "Your are a reviewer, but haven't voted in the current revision"]
query = reviewer:self

[section "Needs final +2"]
query = label:Code-Review>=2 limit:50

[section "Passed Jenkins, No Negative Core Feedback"]
query = NOT label:Code-Review>=2 NOT((reviewerin:neutron-lbaas-core project:openstack/neutron-lbaas OR reviewerin:neutron-vpnaas-core project:openstack/neutron-vpnaas OR reviewerin:neutron-fwaas-core project:openstack/neutron-fwaas) label:Code-Review<=-1) limit:50

[section "Wayward Changes (Changes with no code review in the last 2days)"]
query = NOT label:Code-Review<=2 age:2d
