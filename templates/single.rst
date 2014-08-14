`{{ title }}`_
==============================================================================

{% if description %}
Description::

    {{ description }}
{%- endif %}

URL::

    {{ url }}

{% if configuration %}
Configuration::

{% for line in configuration.splitlines() %}
    {{ line }}
{%- endfor %}
{% endif %}

.. _{{ title }}: {{ url }}
