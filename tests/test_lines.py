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

import codero.strategy.lines


def test_lines_bachelor75page18():
    source = power.link(power.BACHELOR075_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=18,
        horizontals=True,
    )
    page18 = ptcn[0]
    parsed = codero.strategy.lines.parse(page18)
    assert len(parsed.content) == 1
    assert parsed.page == 18
