__NAME__

`qu` - music streaming service backend

__DESCRIPTION__

This is work in progress. The goal is to create a simple and
straight forward music streaming service for your own cloud.

__REQUIREMENTS__

* Python 3
* [Mutagen](https://github.com/quodlibet/mutagen)

__DEPLOYMENT__

    $ nano qu_config.py      # configure library_root
    $ python -m qu --syncdb  # synchronize the music file database
    # python -m qu --web     # run the web app
