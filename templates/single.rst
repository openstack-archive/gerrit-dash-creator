`{{ title }}`_
==============================================================================

{% if description %}
Description
-----------
{{ description }}
{%- endif %}

URL
---

::

   {{ url }}

`View this dashboard <{{ url }}>`__

{% if configuration %}
Configuration
-------------

::

{% for line in configuration.splitlines() %}
    {{ line }}
{%- endfor %}
{% endif %}

.. _{{ title }}: {{ url }}
