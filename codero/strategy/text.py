# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import elements
import iamraw
import texmex
import utila

import codero.data


def parse(ptn: texmex.PageTextContentNavigator) -> iamraw.PageContent:
    content = linenumbers_and_caption(ptn)
    result = iamraw.PageContent(content=content, page=ptn.page)
    return result


def linenumbers_and_caption(ptn):
    code = []
    collector = DetectorLineNumbers()
    for index, line in enumerate(ptn):
        done = collector.run(line, index)
        if not done:
            continue
        # detected
        code.append(done)
        collector.reset()
    content = [
        codero.data.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[1], done[2])),
            tokens=set(utila.ranged_tuple(done[0], done[1])),
        ) for done in code
    ]
    return content


CODE_NUMBER = re.compile(r'^\d{1,3}')


class DetectorLineNumbers:
    """\
    1 $ ./spark-shell
    2 [...]
    3 / __/__ ___ _____/ /__

    Listing 2.1: Word Count in der Spark Konsole
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

    def run(self, line, index):
        text = line.text.strip()
        if self.start is None:
            if CODE_NUMBER.search(text):
                self.start = index
            return None
        if CODE_NUMBER.search(text):
            self.middle = index + 1
            return None
        if elements.iscaption_code(text):
            self.middle = index
            self.end = index + 1
        else:
            self.reset()
            return None
        return self.start, self.middle, self.end

    def reset(self):
        self.start, self.middle, self.end = None, None, None
