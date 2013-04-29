# MLS Stats API

Scrapes and stores MLSSoccer.com statistics. 

### Installation

In order to install clone this repo, and run:

    python setup.py install

Then add `mls_api` to your list of INSTALLED_APPS in your Django project. Then 
just run:

    python manage.py migrate mls_api

to add the necessary tables to your database. 

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


