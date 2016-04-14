__NAME__

`qu` - music streaming service backend

__DESCRIPTION__

This is work in progress. The goal is to create a simple and
straight forward music streaming service for your own cloud.

__REQUIREMENTS__

* Python 3
* [Mutagen](https://github.com/quodlibet/mutagen)
* [Flask](http://flask.pocoo.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/)

__DEPLOYMENT__

    $ git clone https://github.com/NiklasRosenstein/qu.git
    $ cd qu
    $ virtualenv -p python3 env
    $ pip install -r requirements.txt
    $ nano qu_config.py      # configure library_root
    $ python -m qu --syncdb  # synchronize the music file database
    # python -m qu --web     # run the web app

__CREDITS__

    qu/web/static/img/nocover.png: http://gouki113.deviantart.com/art/No-Album-Art-145001929
    qu/web/static/img/check.png,
    qu/web/static/img/error.png: https://www.iconfinder.com/paomedia
