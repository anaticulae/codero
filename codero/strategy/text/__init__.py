# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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
import utilo

import codero.loc
import codero.strategy.text.numbers


def parse(ptn: texmex.PTCN) -> iamraw.PageContent:
    pagenumber = ptn.page
    collected = []
    if content := codero.strategy.text.numbers.linenumbers_and_caption(ptn):
        collected.extend(content)
    ptn = hide_result(ptn, collected)
    if content := codero.strategy.text.numbers.code_without_caption(ptn):
        collected.extend(content)
    ptn = hide_result(ptn, collected)
    if not collected:
        collected = raw_code(ptn)
    pagecontent = iamraw.PageContent(
        content=collected,
        page=pagenumber,
    )
    return pagecontent


def hide_result(ptn, codes):
    done = set()
    for item in codes:
        done |= item.caption
        done |= item.tokens
    ptn = ptn[:]
    for item in done:
        ptn[item] = texmex.TextInfo(text='')
    return ptn


NOHEADLINE = '<<<NOHEADLINE>>>'

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
        iamraw.PeaceOfCode(tokens=set(utilo.rtuple(done[1], done[2])))
        if done[0] == NOHEADLINE else iamraw.PeaceOfCode(
            caption=set(utilo.rtuple(done[0], done[1])),
            tokens=set(utilo.rtuple(done[1], done[2])),
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
