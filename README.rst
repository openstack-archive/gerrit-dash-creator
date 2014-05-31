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

Contributions Welcomed
======================

If you have a dashboard definition that your OpenStack team finds
useful, please just send a PR. Very happy to include many many
interesting examples in this repository for instances that people can
find and use.
