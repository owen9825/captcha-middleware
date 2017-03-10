# -*- coding: utf-8 -*-

from captchaMiddleware.middleware import CaptchaMiddleware
import locale
from unittest import TestCase
import os

TEST_PAGE = os.path.join(os.path.dirname(__file__), 'testPage.html');
TEST_URL = "https://images-na.ssl-images-amazon.com/captcha/fmvtfjch/Captcha_eotjcochkq.jpg";

class ParsingTest(TestCase):

    def openTestPage(self):
        # Todo: spam Amazon until we get a CAPTCHA, then download that page
        testPage = open(TEST_PAGE);
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8');
        return testPage;

    def testFormSearch(self):
        sampleMiddleware = CaptchaMiddleware();
        captchaField = sampleMiddleware.findCaptchaField(self.openTestPage());
        self.assertTrue(captchaField == "field-keywords");

    def testUrlSearch(self):
        sampleMiddleware = CaptchaMiddleware();
        captchaUrl = sampleMiddleware.findCaptchaUrl(self.openTestPage());
        self.assertTrue(captchaUrl == TEST_URL);