# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter
from pytesseract import image_to_string
import urllib
import cStringIO
import numpy as np
from string import ascii_uppercase
import random
import logging
import cv2
import imutils

VOCABULARY = filter(lambda letter: letter != "O", ascii_uppercase);

UNSHARP_FILTER = ImageFilter.UnsharpMask(radius=3, threshold=1);
CAPTCHA_LENGTH = 6;
THRESHOLD = 255 - 30;

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

def adjustAngle(angle):
    """Adjust an angle to something more reasonable"""
    if angle < 0:
        if abs(angle+90) < abs(angle):
            # rotated too far
            return angle + 90;
        else:
            return angle;
    else:
        if abs(angle-90) < angle:
            # rotated too far
            return angle - 90;
        else:
            return angle;

def solveCaptcha(imgUrl, brazen=False):
    result = applyOcr(imgUrl);
    if isPossible(result):
        return result;
    elif brazen:
        # Guess something
        result = adjustSuggestion(result);
        logging.debug("CAPTCHA was adjusted to %s", result);
        return result;
    else:
        return None;

def applyOcr(imgUrl):
    response = urllib.urlopen(imgUrl);
    img = np.asarray(bytearray(response.read()), dtype="uint8");
    src = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE);
    # if it's black on white:
    src = 255 - src;
    _, mask = cv2.threshold(src, THRESHOLD, 255, cv2.THRESH_BINARY);
    mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
    coloured = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB);
    letters = {};
    for c, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour); # this is used for the angle
        # rect is a tuple: ((corner 1, corner2), angle)
        angle = adjustAngle(rect[-1]);
        letterMask = np.zeros(mask.shape, dtype="uint8");
        letterMask = cv2.drawContours(letterMask, [contour], contourIdx=0, color=255, thickness=-1);
        imgROI = cv2.bitwise_and(src, src, mask=letterMask);        
        coloured = cv2.cvtColor(imgROI, cv2.COLOR_GRAY2RGB);
        rotated = imutils.rotate_bound(coloured, -angle);
        rotated = 255 - rotated;
        pilImg = Image.fromarray(rotated);
        charResult = image_to_string(pilImg, config="-psm 10");
        print(charResult);
        if charResult is not None and len(charResult) > 0:
            moments = cv2.moments(contour);
            xCentre = int(moments["m10"]/moments["m00"]);
            while xCentre in letters:
                xCentre += 1; # Avoid key clash
            letters[xCentre] = charResult.upper();
        else:
            logging.debug("No result for character %d", c);
    # Adjust letters based on X axis
    wordSolution = "";
    for xCentre in sorted(letters.keys()):
        wordSolution += letters[xCentre];
    logging.debug("OCR saw %s", wordSolution);
    return wordSolution;
