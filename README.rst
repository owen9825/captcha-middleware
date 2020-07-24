.. image:: https://media.giphy.com/media/S0hxMGYFhEMzm/giphy.gif
    :alt: I must be a robot then

captchaMiddleware
=====================

Checks for a CAPTCHA test and tries solving it. This is open-source so as to prevent slaves from
being forced to solve CAPTCHA tests.

Installation
------------
Note that this program relies on `Tesseract v4
<https://github.com/tesseract-ocr/tesseract/wiki/Compiling/>`_, which is available on Ubuntu 18.04.

Install Tesseract and the language file

::

     sudo apt-get install tesseract-ocr
     sudo mkdir /usr/local/share/tessdata
     wget https://github.com/tesseract-ocr/tessdata/raw/4.00/eng.traineddata
     sudo mv eng.traineddata /usr/local/share/tessdata
     sudo chmod a+w /usr/local/share/tessdata/eng.traineddata
     export TESSDATA_PREFIX=/usr/local/share/tessdata
     which tesseract

Make sure to include the `TESSDATA_PREFIX` in your bash profile.

Install Pillow in Python to substitute for PIL

::

     pip install pillow

Install captchaMiddleware

::

     python setup.py test
     python setup.py install

If the tests fail, test your tesseract installation:

::

    tesseract "unknown letter 0.jpg" prediction --psm 10 --oem 0


Configuration
-------------

Include this in the Downloader Middleware

::

    DOWNLOADER_MIDDLEWARES = {
        …
        'captchaMiddleware.middleware.CaptchaMiddleware':500
    }



In your spider, set a meta key to prevent trying the tests too many times:
::

     from captchaMiddleware.middleware import RETRY_KEY
     …
     def start_requests(self):
          …
          for url in urls:
               yield scrapy.Request(url=url, callback=self.parse,
                    errback=self.errorHandler, meta={RETRY_KEY:0})
