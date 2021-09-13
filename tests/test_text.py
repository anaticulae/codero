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
import utila

import codero.strategy.text


def test_text_bachelor67page11():
    source = power.link(power.BACHELOR067_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=11,
    )
    page11 = ptcn[0]
    parsed = codero.strategy.text.parse(page11)
    assert len(parsed.content) == 1
    assert parsed.page == 11
    code = parsed.content[0].tokens
    caption = parsed.content[0].caption
    assert len(code) == 18
    assert caption == {27}


def test_text_bachelor67page20():
    """Code does not start with number 1. This code forwards code from
    page before.

    TODO: INTRODUCE PAGE CODE MERGER
    """
    source = power.link(power.BACHELOR067_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=20,
    )
    page20 = ptcn[0]
    parsed = codero.strategy.text.parse(page20)
    code = parsed.content[0].tokens
    caption = parsed.content[0].caption
    assert len(code) == 10
    assert caption == {10}


def test_text_bachelor67all():
    source = power.link(power.BACHELOR067_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=(11, 18, 20, 43, 47, 59, 60, 61),
    )
    codes = [len(codero.strategy.text.parse(page).content) for page in ptcn]
    # 11, 17, 18, 20, 42, 47, 59, 60, 61
    expected = [1, 2, 1, 1, 1, 2, 2, 2]  # TODO: VALIDATE LATER
    assert codes == expected


def test_text_bachelor241page156():
    source = power.link(power.BACHELOR241_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=156,
    )
    page156 = ptcn[0]
    parsed = codero.strategy.text.parse(page156)
    # 2 block auf code
    assert len(parsed.content) == 2
    assert parsed.content[0].caption == {14}
    assert parsed.content[0].tokens == {15, 16, 17, 18, 19, 20, 21, 22, 23, 24}
    assert parsed.content[1].caption == {33}
    assert parsed.content[1].tokens == {34, 35, 36}


def test_text_bachelor241all():
    source = power.link(power.BACHELOR241_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=utila.ranged_tuple(200, 240),
    )
    codes = [len(codero.strategy.text.parse(page).content) for page in ptcn]
    expected = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0
    ]  # NOT VALIDATED
    assert codes == expected
