# -*- coding: utf-8 -*-

from scrapy.http import FormRequest
import logging
import locale
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__);

KEYWORDS = {"en":["characters", "type"]};
RETRY_KEY = 'captcha_retries';

class CaptchaMiddleware(object):
    """Checks a page for a CAPTCHA test and, if present, submits a solution for it"""
    MAX_CAPTCHA_ATTEMPTS = 2;

    def containsCaptchaKeywords(self, text):
        # Check that the form mentions something about CAPTCHA
        language, encoding = locale.getlocale(category=locale.LC_MESSAGES);
        if language is None:
            language = KEYWORDS.keys()[0]; # Must be American
        if language[0:2] in KEYWORDS.keys():
            for keyword in KEYWORDS[language[0:2]]:
                if keyword in text.lower():
                    return True;
            return False;
        else:
            logger.warning("CAPTCHA keywords have not been set for this locale.");
            return None;

    def findCaptchaUrl(self, page):
        soup = BeautifulSoup(page, 'lxml');
        images = soup.find_all("img");
        forms = soup.find_all("form");
        if len(forms) != 1 or len(images) == 0:
            # Assert that a CAPTCHA page only has one form: the CAPTCHA form
            # Assert that the CAPTCHA image is tagged as <img>
            return None;
        if not self.containsCaptchaKeywords(forms[0].text):
            return None;
        possibleImages = [];
        for image in images:
            if image in forms[0].descendants:
                possibleImages.append(image);
        if len(possibleImages) > 1:
            # todo: use NLP on the URLs or something. Amazon writes "Captcha" there
            logger.error("To do: resolve ambiguity when multiple images appear \
                in the CAPTCHA form. Maybe this wasn't a CAPTCHA form.");
            return None;
        elif len(possibleImages) == 0:
            logger.warning("Unable to find an image in the CAPTCHA form. Maybe \
                this wasn't a CAPTCHA form.");
            return None;
        # Now grab the URL from the only possible img
        imgUrl = possibleImages[0]["src"];
        return imgUrl;

    def findCaptchaField(self, page):
        soup = BeautifulSoup(page, 'lxml');
        forms = soup.find_all("form");
        if len(forms) != 1:
            logger.debug("Unable to find a form on this page.");
            return None;
        formFields = forms[0].find_all("input");
        possibleFields = filter(lambda field: field["type"] != "hidden", formFields);
        if len(possibleFields) > 1:
            logger.error("Ambiguity when finding form field for CAPTCHA.");
            # Maybe we could use NLP to decide
            return None;
        elif len(possibleFields) == 0:
            logger.error("Unable to find CAPTCHA form field.");
            return None;
        else:
            return possibleFields[0]["name"];

    def process_response(self, request, response, spider):
        captchaUrl = self.findCaptchaUrl(response.text);
        if captchaUrl is None:
            return response; # No CAPTCHA is present
        elif request.meta.get(RETRY_KEY, self.MAX_CAPTCHA_ATTEMPTS) == self.MAX_CAPTCHA_ATTEMPTS:
            logger.warning("Too many CAPTCHA attempts; surrendering.");
            raise IgnoreRequest;
        captchaSolution = solveCaptcha(url = captchaUrl, brazen=True);
        if captchaSolution is None:
            logger.error("CAPTCHA page detected, but no solution was proposed.");
            raise IgnoreRequest;
        # Return a request to submit the captcha
        logger.info("Submitting solution {0:s} for CAPTCHA at {1:s}".format(captchaSolution,
            captchaUrl));
        response.meta[RETRY_KEY] = request.meta.get('captcha_retries', 0) + 1;
        return FormRequest.from_response(response, formnumber=0,
                formdata={findCaptchaField(response.text):captchaSolution});

