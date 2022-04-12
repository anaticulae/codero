# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import codero
import tests

ARCHIVE = utila.join(codero.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR067_PDF, id='bachelor067'),
    pytest.param(power.BACHELOR075_PDF, id='bachelor075'),
    pytest.param(power.BACHELOR090_PDF, id='bachelor090'),
    pytest.param(power.BACHELOR111_PDF, id='bachelor111'),
])
def test_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source,
        testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            step='',
            pages=':',
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.generated = power.link(source)

    def frompath(self, workdir):  # pylint:disable=no-self-use
        loaded = serializeraw.load_codes(workdir)
        return loaded

    def raw(self, value) -> str:
        collected = []
        ptcns = serializeraw.ptcn_frompath(
            self.generated,
            prefix='oneline',
            horizontals=False,
        )
        for page in value:
            ptcn = utila.select_page(ptcns, page.page)
            collected.append(rawpage(ptcn, page))
        result = utila.NEWLINE.join(collected)
        result = result.rstrip()
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
    header = f'################################# {pagenr} #################################\n'
    result = header + utila.NEWLINE.join(collected) + utila.NEWLINE * 4
    return result
