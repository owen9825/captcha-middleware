# -*- coding: utf-8 -*-

from captchaMiddleware.solver import *
from unittest import TestCase
import os
import logging

TEST_PAGE = os.path.join(os.path.dirname(__file__), 'testPage.html')
TEST_IMAGE = os.path.join(os.path.dirname(__file__), "Captcha_eotjcochkq.jpg")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ImageTest(TestCase):
    
    def test_Adjustment(self):
        suggestion = "ABCDE"
        adjusted = adjustSuggestion(suggestion)
        self.assertTrue(len(adjusted) > len(suggestion))
        self.assertTrue(len(adjusted) == CAPTCHA_LENGTH)
        return

    def test_ImageSolving(self):
        logging.info("Opening test image from %s", TEST_IMAGE)
        solution = applyOcr(TEST_IMAGE)
        self.assertTrue(solution == "TAFPLH")
        return
