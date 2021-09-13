# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw


def run(strategy, resource, pages: tuple = None, horizontals: bool = False):
    source = power.link(resource)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=pages,
        horizontals=horizontals,
    )
    if isinstance(pages, int):
        result = strategy(ptcn[0])
    else:
        result = [strategy(page) for page in ptcn]
    return result
