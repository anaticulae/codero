# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila


def run(codes: iamraw.PeaceOfCodes, ptns):
    codes = insert_code_boundings(codes, ptns)
    codes = horizontals_remove(codes, ptns)
    return codes


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
