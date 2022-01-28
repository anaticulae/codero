# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import codero.strategy.lines
import codero.strategy.text

STRATEGIES = [
    codero.strategy.lines.parse,
    codero.strategy.text.parse,
]


def run(navigators: texmex.PageTextContentNavigators):
    work = [[strategy(page) for page in navigators] for strategy in STRATEGIES]
    # remove empty page parsing
    noempty = [[page for page in result if page.content] for result in work]
    best = decide(noempty, navigators)
    return best


def decide(results, ptns):
    best = results[0]
    for item in results[1:]:
        if score(item) > score(best):
            best = item
    best = insert_code_boundings(best, ptns)
    best = horizontals_remove(best, ptns)
    return best


def score(result) -> int:
    """Count number of detected lines of code and comments."""
    count = 0
    for item in result:
        count += len(item.content)
    return count


def insert_code_boundings(codes: iamraw.PeaceOfCodes, ptns):
    for page in codes:
        ptn = utila.select_page(ptns, page=page.page)
        for code in page.content:
            for caption in code.caption:
                code.caption_bounding.append(tuple(ptn[caption].bounding))
            for token in code.tokens:
                code.tokens_bounding.append(tuple(ptn[token].bounding))
    return codes


def horizontals_remove(codes: iamraw.PeaceOfCodes, ptns):
    """Adjust indexes of caption and token to ptns without horizontals."""
    for page in codes:
        ptn = utila.select_page(ptns, page=page.page)
        before = horizontals_before(ptn)
        for code in page.content:
            code.caption = {item - before[item] for item in code.caption}
            code.tokens = {item - before[item] for item in code.tokens}
    return codes


def horizontals_before(ptn):
    before = 0
    result = []
    for item in ptn:
        result.append(before)
        if item.text == texmex.HORIZONTAL:
            before += 1
    return result
