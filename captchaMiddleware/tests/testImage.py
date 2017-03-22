# -*- coding: utf-8 -*-

from captchaMiddleware.solver import *
import locale
from unittest import TestCase
import os
import cv2

TEST_PAGE = os.path.join(os.path.dirname(__file__), 'testPage.html');
TEST_URL = "https://images-na.ssl-images-amazon.com/captcha/fmvtfjch/Captcha_eotjcochkq.jpg";

class ImageTest(TestCase):
    
    def test_Adjustment(self):
        suggestion = "ABCDE";
        adjusted = adjustSuggestion(suggestion);
        self.assertTrue(len(adjusted) > len(suggestion));
        self.assertTrue(len(adjusted) == CAPTCHA_LENGTH);
        return;

    # why is this test being skipped?
    def test_ImageSolving(self):
        solution = applyOcr(TEST_URL);
        self.assertTrue(solution == "TAFPLH");
        return;