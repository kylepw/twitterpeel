===========
twitterpeel
===========

*twitterpeel* is a Twitter frontend API scraper based on Kenneth Reitz's
twitter-scraper_. I originally wrote it because *twitter-scraper* was not
compatible with Python 3.7.

.. _twitter-scraper: https://github.com/kennethreitz/twitter-scraper
.. _requests-html: https://html.python-requests.org

Features
--------
- No Twitter API authentication necessary.
- Fast.

Requirements
------------
- Python 3.6 or higher

Installation
------------
::

	$ pip3 install twitterpeel

or

::

    $ git clone git@github.com:kylepw/twitterpeel.git && cd twitterpeel

Usage
-----
::

    >>> from twitterpeel import get_tweets
    >>>
    >>> for t in get_tweets('MISTERMORT', pages=3):
    ...     print(t['tweetid'], t['text'])
    ...
    1108565146019000321 i wonder if neiman marcus missed me...
    1108521311863738369 Today is the day of spring equinox AND a full moon...
    1108442303465697281 forgot what i was going to say
    ...

License
-------
`MIT License <https://github.com/kylepw/twitterpeel/blob/master/LICENSE>`_
