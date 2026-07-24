# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utilo


def decide(horizontal, text):
    data = (horizontal, text)
    result = []
    for pagenumber, (horizontalx, textx) in utilo.sync_pages(iterators=data,):
        horizontalx = horizontalx.content if horizontalx else []
        textx = textx.content if textx else []
        best = horizontalx if score(horizontalx) > score(textx) else textx
        result.append(iamraw.PageContent(content=best, page=pagenumber))
    return result


def score(items) -> int:
    result = 0
    for item in items:
        result += len(item.caption)
        result += len(item.tokens)
    return result
