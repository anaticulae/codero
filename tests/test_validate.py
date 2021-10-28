# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

CODE = os.path.join(codero.ROOT, 'tests/validate')
read_code = lambda x: utila.file_read(os.path.join(CODE, x)).strip()  # pylint:disable=C0103


@pytest.mark.parametrize(
    'source, expected',
    [
        pytest.param(power.BACHELOR067_PDF, 'bachelor067', id='bachelor067'),
    ],
)
def test_validate(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.run(f'-i {source} -o {testdir.tmpdir}', monkeypatch=monkeypatch)
    loaded = serializeraw.load_codes(testdir.tmpdir)
    if expected is None:
        return
    expected = read_code(expected)
    current = raw(source, loaded)
    if current != expected:
        utila.file_create('baseline', current)
    assert current == expected


def raw(source, extracted) -> str:
    collected = []
    ptcns = serializeraw.ptcn_frompath(
        source,
        prefix='oneline',
        horizontals=True,
    )
    for page in extracted:
        ptcn = utila.select_page(ptcns, page.page)
        collected.append(rawpage(ptcn, page))
    result = utila.NEWLINE.join(collected)
    return result


def rawpage(ptcn, page) -> str:
    pagenr = page.page
    content = page.content
    collected = []
    for poc in content:
        code = utila.NEWLINE.join(ptcn[it].text.strip() for it in poc.tokens)
        captio = utila.NEWLINE.join(ptcn[it].text.strip() for it in poc.caption)
        collected.append('TOKENS:\n' + code)
        collected.append('CAPTION:\n' + captio)
    header = f'############ {pagenr} ############\n'
    result = header + utila.NEWLINE.join(collected)
    return result
