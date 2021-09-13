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


def test_lines_bachelor75all():
    source = power.link(power.BACHELOR075_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=(18, 43, 47, 48, 53, 54, 57, 62),
        horizontals=True,
    )
    codes = [len(codero.strategy.lines.parse(page).content) for page in ptcn]
    expected = [1, 1, 1, 2, 1, 1, 2, 1]
    assert codes == expected


def test_lines_bachelor111page35():
    source = power.link(power.BACHELOR111_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=(35,),
        horizontals=True,
    )
    page35 = ptcn[0]
    parsed = codero.strategy.lines.parse(page35)
    assert len(parsed.content) == 1
    assert parsed.page == 35


def test_lines_bachelor111all():
    source = power.link(power.BACHELOR111_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=(35, 45, 56, 57, 60, 62, 65),
        horizontals=True,
    )
    codes = [len(codero.strategy.lines.parse(page).content) for page in ptcn]
    # HINT: Page 60 is incomplete, therefore the current strategy can not
    # parse this linting.
    # expected = [1, 1, 2, 1, 1, 1, 1]
    expected = [1, 1, 2, 1, 0, 1, 1]
    assert codes == expected
