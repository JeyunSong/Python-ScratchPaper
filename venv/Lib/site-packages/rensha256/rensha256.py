# -*- coding: utf-8 -*-

__version__ = "0.1.78"

from hashlib import sha256
import sys
import os
import logging
import pathlib


def main():
    logger = logging.getLogger('rensha256')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('rensha256.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    fileList = []

    # get file list from stdin if there are any
    if not sys.stdin.isatty():
        fileList = sys.stdin.readlines()

    # get more file names that are arguments
    fileList += sys.argv[1:]

    fileList = [i.strip() for i in fileList]

    logger.debug(f'file list: {",".join(fileList)}')

    for path in fileList:
        original = pathlib.Path(path)
        original.resolve()

        if not os.path.exists(original.absolute()):
            logger.warn("file %s not found" % path)
            continue

        if os.path.isdir(original.absolute()):
            logger.warn(
                'skipping directory %s.  I wasnt meant to process directories.' %
                (original.absolute()))
            continue

        logger.debug("original file %s exists" % path)

        f = open(path, 'rb')
        with f:
            sha = sha256(f.read()).hexdigest()
        newfile = '%s%s' % (sha, original.suffix)
        newpath = os.path.join(original.parent.absolute(), newfile)
        logger.debug('sha256: %s' % sha)
        logger.debug('directory: %s' % original.parent.absolute())
        logger.debug('extension: %s' % original.suffix)
        if original.stem.startswith('.'):
            logger.warn(
                'skipping file %s because it doesnt have an extension' %
                (original.absolute(), newpath))
        if os.path.exists(newpath):
            logger.warn(
                'skipping file %s because target destination already exists %s' %
                (original.absolute(), newpath))
        else:
            logger.debug(
                'moving "%s" to "%s"' %
                (original.absolute(), newpath))
            os.rename(path, newpath)
