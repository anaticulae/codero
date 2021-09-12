# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import codero.data
import iamraw
import texmex


def parse(ptn: texmex.PageTextContentNavigator) -> iamraw.PageContent:
    code = []
    collector = Detector()
    minus = 0
    for index, line in enumerate(ptn):
        done = collector.run(line, index - minus)
        if not done:
            continue
        # detected
        code.append(done)
        minus += 3
        collector.reset()
    converted = [
        codero.data.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[0], done[1])),
            tokens=set(utila.ranged_tuple(done[1], done[2])),
        ) for done in code
    ]
    result = iamraw.PageContent(content=converted, page=ptn.page)
    return result


class Detector:
    start: int = None
    middle: int = None
    end: int = None

    def run(self, line, index):
        text = line.text
        if self.start is None:
            if text == texmex.HORIZONTAL:
                self.start = index
            return None
        if self.middle is None:
            if text == texmex.HORIZONTAL:
                self.middle = index - 1
            return None
        if text != texmex.HORIZONTAL:
            return None
        self.end = index - 2
        return self.start, self.middle, self.end

    def reset(self):
        self.start, self.middle, self.end = None, None, None
