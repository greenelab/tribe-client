====================
Tribe Client
====================

Tribe client is a portable Python app to connect your bioinformatics server
or tool to the 'Tribe' web service (located at https://tribe.greenelab.com).

This package allows web servers created using
`Django <https://docs.djangoprojects.com/en/dev/>`_ to connect directly
to Tribe and make use of its resources. Users of the client web server or tool
can access their Tribe resources via Tribe `OAuth2 <http://oauth.net/2/>`_
authentication.


Download and Install
---------------------
Tribe-client is registered as "tribe-client" in PyPI and is pip
installable:

.. code-block:: shell

	pip install tribe-client



Quick Start with Django
------------------------


1. Add ``tribe_client`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'tribe_client',
    )


2. Include the tribe-client URLconf in your project's URLconf (usually
``urls.py``):

.. code-block:: python

    from django.conf.urls import url, patterns, include

    urlpatterns = patterns('',
      ...
      (r'^tribe_client/', include('tribe_client.urls')),
    )


3. Register your client server at
https://tribe.greenelab.com/oauth2/applications/. Make sure to:

  a. Be logged-in using your Tribe account
  b. Select "Confidential" under ``Client type`` and
  c. Select "Authorization Code" under ``Authorization grant type``
  d. Enter your client server's address plus "/tribe_client/get_token" in the ``Redirect uris`` box. If your client server's current address is http://example.com, enter **http://example.com/tribe_client/get_token**

  .. note:: Currently, Tribe supports the following ``Authorization grant types``:

      * Authorization code
      * Resource owner password-based

    and does not support the following:

      * Implicit
      * Client credentials


4. Write down the Client ID in the ``TRIBE_ID`` setting and the Client secret
in the ``TRIBE_SECRET`` setting in your ``settings.py`` file like so:

.. code-block:: python

    TRIBE_ID = '*****Tribe Client ID*****'
    TRIBE_SECRET = '*****Tribe Client Secret*****'


5. The ``TRIBE_REDIRECT_URI`` setting should be the address of the client
server plus "/tribe_client/get_token".

.. code-block:: python

    TRIBE_REDIRECT_URI = 'http://example.com/tribe_client/get_token'


6. Make sure that you have a base template (which gets extended by your
other templates and contains the ``{% block content %}   {% endblock %}``
statements) that the tribe_client templates can extend, and specify it in
your settings. By default, tribe_client will look for a template
called ``base.html``.

.. code-block:: python

    TRIBE_CLIENT_BASE_TEMPLATE = 'name_of_your_main_template.html'


7. Define in your settings the scope that your client server should have
for Tribe resources. The two options are: 'read' and 'write'.The default
is 'read'. **Note:** The 'write' scope includes the 'read' scope access. 

.. code-block:: python

    TRIBE_SCOPE = 'write'  # Or 'read'


8. Make a link that takes the user to the ``/tribe_client`` url of your website
(e.g. ``http://example.com/tribe_client``) for them to log in using Tribe.


A Closer Look
-----------------------------

Under the hood, tribe-client has functions that:

1) Get an access token (via the `OAuth2 <http://oauth.net/2/>`_ protocol) that
allows users to access and create resources in Tribe.

2) Retrieves public and private collections (and their versions) and displays
them on the client server using views and templates included in the package.

3) Allows users to create new collections and versions remotely, from the
client server.
