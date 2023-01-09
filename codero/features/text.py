# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import codero.finalize
import codero.strategy.text


def work(
    oneline_text: str,
    oneline_textposition: str,
    oneline_font_header: str,
    oneline_font_content: str,
    sizeandborder: str,
    headerfooter: str,
    horizontalx: str,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.ptcn_fromfile(
        oneline_text,
        oneline_textposition,
        sizeandborder,
        headerfooter,
        oneline_font_header,
        oneline_font_content,
        horizontals=horizontalx,
        pages=pages,
    )
    parsed = run(ptcns)
    dumped = serializeraw.dump_codes(parsed)
    return dumped


def run(ptcns) -> list:
    result = []
    for ptn in ptcns:
        parsed = codero.strategy.text.parse(ptn)
        if not parsed.content:
            continue
        result.append(parsed)
    result = codero.finalize.run(result, ptcns)
    return result
