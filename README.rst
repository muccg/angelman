Angelman
========
About
-----

Angelman is a patient registry based on RDRF (https://muccg.github.io/rdrf/). During development, RDRF is installed as a git submodule::

    › git submodule status
    d28dfe3b313c1917dc4d46ac15adf5320d979cc3 rdrf (2.1.7)

Forgetting to update the git submodule is a common dev time error::

    › git submodule update
    Submodule path 'rdrf': checked out 'd28dfe3b313c1917dc4d46ac15adf5320d979cc3'

Refer to RDRF project for more docs.

Email:

rdrf@ccg.murdoch.edu.au

For developers
--------------

We do our development using Docker_ containers.
You will have to set up Docker on your development machine.

Other development dependencies are Python 2 and virtualenv_.

All the development tasks can be done by using the ``develop.sh`` shell script in this directory.
Please run it without any arguments for help on its usage.

A typical usage is::

    ./develop.sh build base
    ./develop.sh build builder
    ./develop.sh build dev
    ./develup.sh up

This will start up all the docker containers needed for dev.  You can then access the application on http://localhost:8000
You can login with one of the default users *admin/admin*.

.. _Docker: https://www.docker.com/
.. _docker-compose: https://docs.docker.com/compose/
.. _devdocs: https://rare-disease-registry-framework.readthedocs.io/en/latest/development.html

Contributing
------------

1. Fork ``next_release`` branch
2. Make changes on a feature branch
3. Submit pull request

