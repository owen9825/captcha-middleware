# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter
from pytesseract import image_to_string
import urllib
import cStringIO
import numpy as np
from string import ascii_uppercase
import random

VOCABULARY = filter(lambda letter: letter != "O", ascii_uppercase);

UNSHARP_FILTER = ImageFilter.UnsharpMask(radius=3, threshold=1);
CAPTCHA_LENGTH = 6;

def isPossible(captchaSolution):
    """Amazon always uses 6 uppercase Latin letters with no accents"""
    if len(captchaSolution) == CAPTCHA_LENGTH:
        for letter in captchaSolution:
            if letter not in VOCABULARY:
                return False;
        return True;
    return False;

def adjustSuggestion(input):
    input = input.upper();
    if len(input) > CAPTCHA_LENGTH:
        # All letters will be filtered for eligibility later. For now though, preserve as much as 
        # possible
        input = filter(lambda letter: letter in VOCABULARY, input);
    while len(input) > CAPTCHA_LENGTH:
        cutLocation = random.randint(0, len(input)-1);
        input = input[0:cutLocation] + input[cutLocation+1:];
    while len(input) < CAPTCHA_LENGTH:
        # Throw in extra, random characters
        insLocation = random.randint(0, len(input));
        input = input[0:insLocation] + random.choice(VOCABULARY) + input[insLocation:];
    result = "";
    # Filter letters for eligibility
    for letter in input:
        if letter in VOCABULARY:
            result += letter;
        else:
            result += random.choice(VOCABULARY);
    return result;

def solveCaptcha(imgUrl, brazen=False):
    imgBlob = cStringIO.StringIO(urllib.urlopen(imgURL).read());
    img = Image.open(imgBlob);
    filtered = img.filter(UNSHARP_FILTER);
    arrayImg = np.asArray(filtered);
    thresholded = np.uint8((arrayImg > THRESHOLD) * 255); # 2⁸-1 := 255
    filtered = Image.fromarray(thresholded);

    result = image_to_string(filtered);
    if isPossible(result):
        return result;
    elif(brazen):
        # Guess something
        result = adjustSuggestion(result);
    else:
        return None;