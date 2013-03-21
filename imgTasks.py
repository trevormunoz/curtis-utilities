#!/usr/bin/env  python

""""
Convert GIF images to PNG using Imagemagick
"""

import os
import subprocess
from celery import Celery

celery = Celery('imgTasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@celery.task
def convert(fname):
    """
    Use Imagemagick to convert file formats
    """
    args = ['convert', fname, '-compress', 'none',
            os.path.splitext(os.path.basename(fname))[0]+'.png']
    prog_status = subprocess.call(args)
    return "{0} processed. Exited with status code {1}".format(
        fname, prog_status)


@celery.task
def ocr(fname):
    """
    Run tesseract ocr engine over file to produce hOCR output
    """
    args = ['tesseract', fname,
            os.path.splitext(os.path.basename(fname))[0], 'hocr']
    prog_status = subprocess.call(args)
    return "{0} processed. Exited with status code {1}".format(
        fname, prog_status)
