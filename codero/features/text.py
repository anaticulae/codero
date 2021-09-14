# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import codero.strategy.decider


def work(
    oneline_text: str,
    oneline_textposition: str,
    oneline_font_header: str,
    oneline_font_content: str,
    sizeandborder: str,
    headerfooter: str,
    horizontals: str,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textposition,
        sizeandborder,
        headerfooter,
        oneline_font_header,
        oneline_font_content,
        horizontals=horizontals,
        pages=pages,
    )
    done = codero.strategy.decider.run(ptcns)
    dumped = serializeraw.dump_codes(done)
    return dumped
