# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import codero.decider


def work(
    horizontalx: str,
    textx: str,
    pages: tuple = None,
) -> str:
    horizontalx = serializeraw.load_codes(
        horizontalx,
        pages=pages,
    )
    textx = serializeraw.load_codes(
        textx,
        pages=pages,
    )
    result = codero.decider.decide(horizontalx, textx)
    dumped = serializeraw.dump_codes(result)
    return dumped
