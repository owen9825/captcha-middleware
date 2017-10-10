.. image:: http://static.fjcdn.com/gifs/When+you+fail+the+captcha_06a12c_5483651.gif
     :target: http://giphy.com/gifs/fail-gaDBMncAI7HEs
     :alt: I must be a robot then

captchaMiddleware
=====================

Checks for a CAPTCHA test and tries solving it. This is open-source so as to prevent slaves from
being forced to solve CAPTCHA tests.

Configuration
-------------

Include this in the Downloader Middleware

::

    DOWNLOADER_MIDDLEWARES = {
        …
        'captchaMiddleware.middleware.CaptchaMiddleware':500
    }

Install Tesseract

::

     sudo apt-get install tesseract-ocr

Install Pillow in Python to substitute for PIL

::
     pip install pillow


In your spider, set a meta key to prevent trying the tests too many times:
::

     from captchaMiddleware.middleware import RETRY_KEY
     …
     def start_requests(self):
          …
          for url in urls:
               yield scrapy.Request(url=url, callback=self.parse,
                    errback=self.errorHandler, meta={RETRY_KEY:0})
