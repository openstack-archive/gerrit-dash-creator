==========================
 Gerrit Dashboard Creator
==========================

Creates custom urls for gerrit dashboards

The Problem
===========

The Gerrit Review system is great, until it gets completely out of
control with too much content in it. When you are staring at a single
list of 400 reviews, it's completely overwhelming.

Sisyphus never had it so good.

The Solution
============

I've found that slicing up the giant review task into a set of smaller
buckets that you can see actually get smaller as you go through them
becomes a far more motivating way of looking at reviews.

As of gerrit 2.6 there is support for building custom dashboards, both
on the server side, and on the client side (as a url). These are
really powerful.

The server side defintion for these dashboards is pretty easy to
understand, however you need really extreme levels of permissions to
create these dashboards. The client side definition is a single url
which is hard to manipulate inline.

This tool takes the server side definition, creates the client side
encoding of it, and spits that url out on the command line. You can
then load it in your browser and off you go.

Usage
=====

It's super easy, just check out the code, and pass it 1 arg, which is
the dash file you want the url for::

  > ./gerrit-dash-creator dashboards/devstack.dash

  URL for Devstack Review Inbox
  https://review.openstack.org/#/dashboard/?foreach=%28project%3Aopenstack-dev%2Fdevstack+OR+project%3Aopenstack-dev%2Fdevstack-vagrant+OR+project%3Aopenstack-dev%2Fbash8+OR+project%3Aopenstack-dev%2Fgrenade%29+status%3Aopen+NOT+owner%3Aself+NOT+label%3AWorkflow%3C%3D-1+label%3AVerified%3E%3D1%2Cjenkins+NOT+label%3ACode-Review%3E%3D0%2Cself&title=Devstack+Review+Inbox&Needs+Feedback+%28Changes+older+than+5+days+that+have+not+been+reviewed+by+anyone%29=NOT+label%3ACode-Review%3C%3D2+age%3A5d&Your+are+a+reviewer%2C+but+haven%27t+voted+in+the+current+revision=NOT+label%3ACode-Review%3C%3D2%2Cself+reviewer%3Aself&Needs+final+%2B2=label%3ACode-Review%3E%3D2+limit%3A50&Passed+Jenkins%2C+No+Negative+Feedback=NOT+label%3ACode-Review%3E%3D2+NOT+label%3ACode-Review%3C%3D-1+limit%3A50&Wayward+Changes+%28Changes+with+no+code+review+in+the+last+2days%29=NOT+label%3ACode-Review%3C%3D2+age%3A2d

Then put the url in your browser and off you go.

Contributions Welcomed
======================

If you have a dashboard definition that your OpenStack team finds
useful, please just send a PR. Very happy to include many many
interesting examples in this repository for instances that people can
find and use.

If you have questions please find me on #openstack-dev,
#openstack-infra, or #openstack-qa on FreeNode to discuss.
