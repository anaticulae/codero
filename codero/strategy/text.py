# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Code Inside Text Detector
=========================

Detect code as a normal part of written text. There are no special
elements which help detecting these lines of code.

1. Strategy: Lines number and caption below
2. Strategy: Specialized R-Code with headline detector
"""

import re

import configo
import elements
import iamraw
import texmex
import utila


def parse(ptn: texmex.PageTextContentNavigator) -> iamraw.PageContent:
    content = linenumbers_and_caption(ptn)
    if not content:
        content = raw_code(ptn)
    result = iamraw.PageContent(content=content, page=ptn.page)
    return result


NOHEADLINE = '<<<NOHEADLINE>>>'


def linenumbers_and_caption(ptn):
    code = []
    collector = DetectorLineNumbers()
    for index, line in enumerate(ptn):
        done = collector.run(line.text, index)
        if not done:
            continue
        # detected
        code.append(done)
        collector.reset()
    content = [
        iamraw.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[1], done[2])),
            tokens=set(utila.ranged_tuple(done[0], done[1])),
        ) for done in code
    ]
    return content


RAWCODE_LENGTH_MIN = configo.HV_INT_PLUS(default=5)


def raw_code(ptn):
    code = []
    collector = DetectorWithHeadline()
    for index, line in enumerate(ptn):
        done = collector.run(line.text, index)
        if not done:
            continue
        # detected
        code.append(done)
        collector.reset()
    if any((collector.start, collector.middle, collector.end)):
        # raw code till page end
        code.append((collector.start, collector.middle, len(ptn)))
    content = [
        iamraw.PeaceOfCode(tokens=set(utila.ranged_tuple(done[1], done[2])))
        if done[0] == NOHEADLINE else iamraw.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[0], done[1])),
            tokens=set(utila.ranged_tuple(done[1], done[2])),
        ) for done in code
    ]

    def is_valid_raw(item):
        if not item.caption:
            if len(item.tokens) < RAWCODE_LENGTH_MIN:
                # Too short code without any caption
                return False
        return True

    content = [item for item in content if is_valid_raw(item)]
    return content


CODE_NUMBER = re.compile(r'^\d{1,3}(?!\.)')


class DetectorLineNumbers:
    """\
    1 $ ./spark-shell
    2 [...]
    3 / __/__ ___ _____/ /__

    Listing 2.1: Word Count in der Spark Konsole

    >>> dtn = DetectorLineNumbers()
    >>> dtn.run('1 import collections', 10)
    >>> dtn.run('2 Abc = collections.namedtuple("Abc a b c")', 11)
    >>> dtn.run('Listing 3: Simple python example', 12)
    (10, 12, 13)
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

    def run(self, line: str, index: int):
        text = line.strip()
        if self.start is None:
            if self.loc(text):
                self.start = index
            return None
        if self.loc(text):
            self.middle = index + 1
            return None
        if self.valid(text):
            self.middle = index
            self.end = index + 1
        else:
            self.reset()
            return None
        return self.final()

    def loc(self, text: str) -> bool:  # pylint:disable=R0201
        """Determine if text can be a line of code."""
        return CODE_NUMBER.search(text)

    def valid(self, text: str) -> bool:  # pylint:disable=R0201
        return elements.iscaption_code(text)

    def final(self):
        result = self.start, self.middle, self.end
        self.reset()
        return result

    def reset(self):
        self.start, self.middle, self.end = None, None, None


RCODE = re.compile(r'^R-Code:')


class DetectorWithHeadline:
    """\
    R-Code:

    > PROB_VOLLST <- NA
    > PROB_VOLLST[PROB_VOLLST_s1 == 1 & PROB_VOLLST_s2 == 1] <- 1
    > PROB_VOLLST[PROB_VOLLST_s1 != 1 | PROB_VOLLST_s2 != 1] <- 0
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

    def run(self, line: str, index: int):
        text = line.strip()
        if self.start is None:
            if RCODE.search(text):
                self.start = index
                return None
            if text and text[0] in '#>+':
                # TODO: MAKE THIS MORE GENERAL
                # R-Code start without headline
                self.start = NOHEADLINE
                self.middle = index
            return None
        if text and text[0] in '#>+':
            if self.middle is None:
                self.middle = index
            else:
                self.end = index + 1
            return None
        if self.middle is not None:
            result = self.start, self.middle, index
            self.reset()
            return result
        self.reset()
        return None

    def reset(self):
        self.start, self.middle, self.end = None, None, None
