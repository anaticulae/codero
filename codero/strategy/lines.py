# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Code Between Lines Detector
===========================

1. Strategy: Code and listings is detected inside 3 horizonals
2. Backup: Code is detected inside 2 horizonals and caption is detected below
"""

import elements
import iamraw
import texmex
import utila


def parse(ptn: texmex.PageTextContentNavigator) -> iamraw.PageContent:
    content = all_inside_textual_horizontals(ptn)
    if not content:
        content = caption_below_code(ptn)
    result = iamraw.PageContent(content=content, page=ptn.page)
    return result


def all_inside_textual_horizontals(ptn):
    """\
    Example

    ---------------------------------------------------------------------------
    Listing 2.1 Eine Beschwerde aus dem NHTSA-Datensatz.
    ---------------------------------------------------------------------------
    WHEN REAR ENDED WITH FOOT ON BRAKE, DRIVERS SHOULDER BELT DIDN’T RESTRAIN
        FROM MAKING CONTACT, RESULTING IN AN INJURY. ESTIMATED SPEED OF
        IMPACT 30 MPH.
    ---------------------------------------------------------------------------
    """
    code = []
    collector = DetectorAllInside()
    for index, line in enumerate(ptn):
        done = collector.run(line, index)
        if not done:
            continue
        if len(utila.make_unique(done)) != 3:
            # false posititve, a lot of lines with any content. We require
            # content between detected lines to have valid code detection.
            collector.reset()
            continue
        # detected
        code.append(done)
        collector.reset()
    converted = [
        iamraw.PeaceOfCode(
            caption=utila.ranged_tuple(done[0] + 1, done[1]),
            tokens=utila.ranged_tuple(done[1] + 1, done[2]),
        ) for done in code
    ]
    content = remove_invalids(converted, ptn)
    return content


def caption_below_code(ptn):
    code = []
    collector = DetectorBelow()
    for index, line in enumerate(ptn):
        done = collector.run(line, index)
        if not done:
            continue
        # detected
        code.append(done)
        collector.reset()
    content = [
        iamraw.PeaceOfCode(
            caption=utila.ranged_tuple(done[1] + 1, done[2] + 1),
            tokens=utila.ranged_tuple(done[0] + 1, done[1]),
        ) for done in code
    ]
    content = remove_invalids(content, ptn)
    return content


def remove_invalids(content, navigator: texmex.PageTextContentNavigator):
    result = []
    for item in content:
        if not item.tokens:
            # skip three horizontals in a row
            continue
        if not item.caption:
            # skip three horizontals in a row
            continue
        firstindex = item.caption[0]
        if not elements.iscaption_code(navigator[firstindex].text):
            continue
        result.append(item)
    return result


class DetectorAllInside:
    """\
    ---------------------------------------------------------------------------
    Listing 2.1 Eine Beschwerde aus dem NHTSA-Datensatz.
    ---------------------------------------------------------------------------
    WHEN REAR ENDED WITH FOOT ON BRAKE, DRIVERS SHOULDER BELT DIDN’T RESTRAIN
        FROM MAKING CONTACT, RESULTING IN AN INJURY. ESTIMATED SPEED OF
        IMPACT 30 MPH.
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
                self.middle = index
            return None
        if text != texmex.HORIZONTAL:
            return None
        self.end = index
        return self.start, self.middle, self.end

    def reset(self):
        self.start, self.middle, self.end = None, None, None


class DetectorBelow:
    """\
    ---------------------------------------------------------------------------
    WHEN REAR ENDED WITH FOOT ON BRAKE, DRIVERS SHOULDER BELT DIDN’T RESTRAIN
        FROM MAKING CONTACT, RESULTING IN AN INJURY. ESTIMATED SPEED OF
        IMPACT 30 MPH.
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
                self.middle = index
            return None
        if not elements.iscaption_code(text):
            # invalid parsing, reset Detector
            self.reset()
            return None
        self.end = index
        return self.start, self.middle, self.end

    def reset(self):
        self.start, self.middle, self.end = None, None, None
