# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import codero
import tests
import tests.utils

CODE = os.path.join(codero.ROOT, 'tests/validate')
read_code = lambda x: utila.file_read(os.path.join(CODE, x)).strip()  # pylint:disable=C0103


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR067_PDF, 'bachelor067', id='bachelor067'),
    pytest.param(power.BACHELOR075_PDF, 'bachelor075', id='bachelor075'),
    pytest.param(power.BACHELOR111_PDF, 'bachelor111', id='bachelor111'),
])
def test_validate(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.run(f'-i {source} -o {testdir.tmpdir}', monkeypatch=monkeypatch)
    loaded = serializeraw.load_codes(testdir.tmpdir)
    if expected is None:
        return
    expected = read_code(expected)
    current = tests.utils.raw(source, loaded)
    if current != expected:
        utila.file_create('baseline', current)
    assert current == expected
