# MLS Stats API

Scrapes and stores MLSSoccer.com statistics. 

### Installation

In order to install clone this repo, and run:

    python setup.py install

Then add:

* `mls_api` 
* `south` 
* `django_nose`

to your list of INSTALLED_APPS in your Django project. Then just run:

    python manage.py syncdb
    python manage.py migrate mls_api

to add the necessary tables to your database. 

### Alternate Installation

While the `mls_api` project can be installed and added to your existing Django
project, you can also use the Django project included in this repo. To do that
you'll simply want to do the following:

* Clone this repo: `git clone https://github.com/f4nt/mls-api`
* `cd` into the `mls-api` directory
* Make use of the `manage.py` file like you would with any Django project, such
as running the `scrape_game` command below.

### Scraper Usage

This app includes a management command that will parse stats from the MLSSoccer.com 
website. There are a couple methods of use:

    python manage.py scrape_game

This method of running the scraper will parse all of the stats from the MLS 
[Results Map](http://www.mlssoccer.com/results) for the current year. Optionally 
you can run with a year argument:

    python manage.py scrape_game --year=2011

If a Result Map doesn't exist for the given year however, this will fail. MLS 
currently only tracks back to 2011. 

If the script encounters a game with a statistics link that already exists it 
will skip that link. You can pass the option of forcing to the script to disable 
this:

    python manage.py scrape_game --force

Finally, you can give the script a specific stats link for it to parse:

    python manage.py scrape_game http://www.example.com/stats

#### Scraper Options

* `-f`, `--force`: Forces the scraper to overwrite existing games.
* `-y`, `--year`: Year of competition to parse
* `-w`, `--workers`: Number of worker threads to parse with (Default: 5)
