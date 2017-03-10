.. image:: http://static.fjcdn.com/gifs/When+you+fail+the+captcha_06a12c_5483651.gif
     :target: http://giphy.com/gifs/fail-gaDBMncAI7HEs
     :alt: I must be a robot then

captchaMiddleware
=====================

Checks for a CAPTCHA test and tries solving it

Configuration
-------------

Turn off the built-in ``UserAgentMiddleware`` and add
``RandomUserAgentMiddleware``.

In Scrapy >=1.0:

::

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    }

In Scrapy <1.0:

::

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    }
