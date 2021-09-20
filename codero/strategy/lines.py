# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import iamraw
import texmex
import utila


def parse(ptn: texmex.PageTextContentNavigator) -> iamraw.PageContent:
    content = all_inside_lines(ptn)
    if not content:
        content = caption_below(ptn)
    result = iamraw.PageContent(content=content, page=ptn.page)
    return result


def all_inside_lines(ptn):
    code = []
    collector = DetectorAllInside()
    minus = 0
    for index, line in enumerate(ptn):
        done = collector.run(line, index - minus)
        if not done:
            continue
        if len(utila.make_unique(done)) != 3:
            # false posititve, a lot of lines with any content. We require
            # content between detected lines to have valid code detection.
            collector.reset()
            continue
        # detected
        code.append(done)
        minus += 3
        collector.reset()
    converted = [
        iamraw.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[0], done[1])),
            tokens=set(utila.ranged_tuple(done[1], done[2])),
        ) for done in code
    ]
    content = remove_invalids(converted, ptn)
    return content


def caption_below(ptn):
    code = []
    collector = DetectorBelow()
    minus = 0
    for index, line in enumerate(ptn):
        done = collector.run(line, index - minus)
        if not done:
            continue
        # detected
        code.append(done)
        minus += 2
        collector.reset()
    content = [
        iamraw.PeaceOfCode(
            caption=set(utila.ranged_tuple(done[1], done[2])),
            tokens=set(utila.ranged_tuple(done[0], done[1])),
        ) for done in code
    ]
    return content


def remove_invalids(content, navigator: texmex.PageTextContentNavigator):
    navigator = [
        item.text for item in navigator if item.text != texmex.HORIZONTAL
    ]
    result = []
    for item in content:
        firstindex = list(item.caption)[0]
        first = navigator[firstindex]
        if not elements.iscaption_code(first):
            continue
        result.append(item)
    return result


class DetectorAllInside:
    """\
    ---------------------------------------------------------------------------
    Listing 2.1 Eine Beschwerde aus dem NHTSA-Datensatz.
    ---------------------------------------------------------------------------
    WHEN REAR ENDED WITH FOOT ON BRAKE, DRIVERS SHOULDER BELT DIDN’T RESTRAIN FROM MAKING
        CONTACT, RESULTING IN AN INJURY. ESTIMATED SPEED OF IMPACT 30 MPH.
    ---------------------------------------------------------------------------
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

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


class DetectorBelow:
    """\
    ---------------------------------------------------------------------------
    WHEN REAR ENDED WITH FOOT ON BRAKE, DRIVERS SHOULDER BELT DIDN’T RESTRAIN FROM MAKING
        CONTACT, RESULTING IN AN INJURY. ESTIMATED SPEED OF IMPACT 30 MPH.
    ---------------------------------------------------------------------------
    Listing 2.1 Eine Beschwerde aus dem NHTSA-Datensatz.
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

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
        if not elements.iscaption_code(text):
            # invalid parsing, reset Detector
            self.reset()
            return None
        self.end = index - 2
        return self.start, self.middle, self.end

    def reset(self):
        self.start, self.middle, self.end = None, None, None
