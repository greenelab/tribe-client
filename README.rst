=====
Django Tribe client
=====

Tribe client is a simple Django app to connect your server to the 'Tribe' web service
(located at http://tribe.dartmouth.edu).

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "tribe-client" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = (
        ...
        'tribe-client',
    )

 
2. Include the tribe-client URLconf in your project urls.py like this::

     url(r'^tribe_client/', include('tribe_client.urls')),



