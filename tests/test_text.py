# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import codero.strategy.text
import tests.utils


def test_text_bachelor67page11():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR067_PDF,
        pages=11,
    )
    assert len(parsed.content) == 1
    assert parsed.page == 11
    code = parsed.content[0].tokens
    caption = parsed.content[0].caption
    assert len(code) == 18
    assert caption == {27}


def test_text_bachelor67p40():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR067_PDF,
        pages=40,
    )
    content = parsed.content
    assert len(content) == 1
    assert len(content[0].tokens) == 3


def test_text_bachelor67page41():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR067_PDF,
        pages=41,
    )
    content = parsed.content
    assert len(content) == 2


def test_text_bachelor67page20():
    """Code does not start with number 1.

    This code forwards code from page before.

    TODO: INTRODUCE PAGE CODE MERGER
    """
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR067_PDF,
        pages=20,
    )
    code = parsed.content[0].tokens
    caption = parsed.content[0].caption
    assert len(code) == 10
    assert caption == {10}


def test_text_bachelor67all():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR067_PDF,
        pages=(11, 18, 20, 43, 47, 59, 60, 61),
    )
    codes = [len(page.content) for page in parsed]
    # 11, 17, 18, 20, 42, 47, 59, 60, 61
    expected = [1, 2, 1, 1, 1, 4, 2, 2]  # TODO: VALIDATE LATER
    assert codes == expected


def test_text_bachelor241page156():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR241_PDF,
        pages=156,
    )
    # 2 block auf code
    assert len(parsed.content) == 2
    assert parsed.content[0].caption == {14}
    assert parsed.content[0].tokens == {15, 16, 17, 18, 19, 20, 21, 22, 23, 24}
    assert parsed.content[1].caption == {33}
    assert parsed.content[1].tokens == {34, 35, 36}


def test_text_bachelor241all():
    parsed = tests.utils.run(
        codero.strategy.text.parse,
        resource=power.BACHELOR241_PDF,
        pages=utila.ranged_tuple(200, 240),
    )
    codes = [len(page.content) for page in parsed]
    expected = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0
    ]  # NOT VALIDATED
    assert codes == expected
