# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import tests.utils


@utilatest.requires(power.MASTER110_PDF)
def test_nocodes(td, mp):
    source = power.link(power.MASTER110_PDF)
    tests.run(f'-i {source} -o {td.tmpdir}', mp=mp)
    outpath = td.tmpdir.join('codero__text_text.yaml')
    loaded = serializeraw.load_codes(outpath)
    if loaded:
        utila.log(tests.utils.raw(source, loaded))
    assert not loaded


@pytest.mark.parametrize('source', (
    pytest.param(power.BACHELOR241_PDF, id='bachelor241'),
    pytest.param(power.BACHELOR063_PDF, id='bachelor063'),
))
def test_cli_all(source, td, mp):
    """\
    bachelor063: regression test to skip invalid parsings
    """
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.run(f'-i {source} -o {td.tmpdir}', mp=mp)
    loaded = serializeraw.load_codes(td.tmpdir)
    # ensure that loader is runned correctly
    assert loaded or loaded == []  # pylint:disable=C1803
