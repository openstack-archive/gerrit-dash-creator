========================
Gerrit Dashboard Creator
========================

Creates custom URLs for Gerrit dashboards

The Problem
===========

The Gerrit code review system is great, until it gets completely out of
control with too much content in it. When you are staring at a single
list of 400 reviews, it's completely overwhelming.

Sisyphus never had it so good.

The Solution
============

I've found that slicing up the giant review task into a set of smaller
buckets that you can see actually get smaller as you go through them
becomes a far more motivating way of looking at reviews.

As of Gerrit 2.6 there is support for building custom dashboards, both
on the server side, and on the client side (as a URL). These are
really powerful.

The server side definition for these dashboards is pretty easy to
understand, however you need really extreme levels of permissions to
create these dashboards. The client side definition is a single URL
which is hard to manipulate inline.

This tool takes the server side definition, creates the client side
encoding of it, and spits that URL out on the command line. You can
then load it in your browser and off you go.

Usage
=====

It's super easy, just check out the code, and pass 1 argument, which is
the dashboard file you want the URL for::

  $ ./gerrit-dash-creator dashboards/devstack.dash
  https://review.openstack.org/#/dashboard/?foreach=%28project%3Aopenstack-dev%2Fdevstack+OR+project%3Aopenstack-dev%2Fdevstack-vagrant+OR+project%3Aopenstack-dev%2Fbashate+OR+project%3Aopenstack-dev%2Fgrenade%29+status%3Aopen+NOT+owner%3Aself+NOT+label%3AWorkflow%3C%3D-1+label%3AVerified%3E%3D1%252cjenkins+NOT+label%3ACode-Review%3E%3D0%252cself&title=Devstack+Review+Inbox&&Needs+Feedback+%28Changes+older+than+5+days+that+have+not+been+reviewed+by+anyone%29=NOT+label%3ACode-Review%3C%3D2+age%3A5d&Your+are+a+reviewer%2C+but+haven%27t+voted+in+the+current+revision=NOT+label%3ACode-Review%3C%3D2%2Cself+reviewer%3Aself&Needs+final+%2B2=label%3ACode-Review%3E%3D2+limit%3A50+NOT+label%3ACode-Review%3C%3D-1%2Cself&Passed+Jenkins%2C+No+Negative+Feedback=NOT+label%3ACode-Review%3E%3D2+NOT+label%3ACode-Review%3C%3D-1+limit%3A50&Wayward+Changes+%28Changes+with+no+code+review+in+the+last+2days%29=NOT+label%3ACode-Review%3C%3D2+age%3A2d

Then put the URL in your browser and off you go.

A daily updated index of all available dashboars is available
at http://ghostcloud.net/openstack_gerrit_dashboards/.


Contributions Welcomed
======================

If you have a dashboard definition that your OpenStack team finds
useful, please submit a change request via git-review. The list of
current outstanding changes can be seen at:

https://review.openstack.org/#/q/status:open+project:stackforge/gerrit-dash-creator,n,z

I'm very happy to include additional interesting examples that teams
find useful, and make it possible for teams to explore other
approaches to reviewing code.

If you have questions please find me (sdague) on #openstack-dev,
#openstack-infra, or #openstack-qa on FreeNode to discuss.
