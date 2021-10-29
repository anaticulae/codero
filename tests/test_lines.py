# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import codero.strategy.lines
import tests.utils


def test_lines_bachelor75page18():
    parsed = tests.utils.run(
        codero.strategy.lines.parse,
        resource=power.BACHELOR075_PDF,
        horizontals=True,
        pages=18,
    )
    content = parsed.content
    assert len(content) == 1
    assert parsed.page == 18
    code = content[0]
    # These lines numbers are with horizonals, without (0,); (1, 2)
    assert code.caption == (1,)
    assert code.tokens == (3, 4)


def test_lines_bachelor75all():
    parsed = tests.utils.run(
        codero.strategy.lines.parse,
        resource=power.BACHELOR075_PDF,
        horizontals=True,
        pages=(18, 43, 47, 48, 53, 54, 57, 62),
    )
    codes = [len(page.content) for page in parsed]
    expected = [1, 1, 1, 2, 1, 1, 2, 1]
    assert codes == expected


def test_lines_bachelor111page35():
    parsed = tests.utils.run(
        codero.strategy.lines.parse,
        resource=power.BACHELOR111_PDF,
        horizontals=True,
        pages=35,
    )
    assert len(parsed.content) == 1
    assert parsed.page == 35


def test_lines_bachelor111all():
    parsed = tests.utils.run(
        codero.strategy.lines.parse,
        resource=power.BACHELOR111_PDF,
        horizontals=True,
        pages=(35, 45, 56, 57, 60, 62, 65),
    )
    codes = [len(page.content) for page in parsed]
    # HINT: Page 60 is incomplete, therefore the current strategy can not
    # parse this linting.
    # expected = [1, 1, 2, 1, 1, 1, 1]
    expected = [1, 1, 2, 1, 0, 1, 1]
    assert codes == expected
