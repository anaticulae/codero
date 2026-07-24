# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import codero
import tests

ARCHIVE = utilo.join(codero.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.BACHELOR067_PDF, id='bachelor067'),
    pytest.param(hoverpower.BACHELOR075_PDF, id='bachelor075'),
    pytest.param(hoverpower.BACHELOR090_PDF, id='bachelor090'),
    pytest.param(hoverpower.BACHELOR111_PDF, id='bachelor111'),
    pytest.param(hoverpower.DISS205_PDF, id='diss205'),
])
def test_validate(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source,
        td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(tests.run, mp=mp),
            step='',
            pages=':',
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.generated = hoverpower.link(source)

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
            ptcn = utilo.select_page(ptcns, page.page)
            collected.append(rawpage(ptcn, page))
        result = utilo.NEWLINE.join(collected)
        result = result.rstrip()
        return result


def rawpage(ptcn, page) -> str:
    pagenr = page.page
    content = page.content
    collected = []
    for poc in content:
        code = utilo.NEWLINE.join(ptcn[it].text.strip() for it in poc.tokens)
        captio = utilo.NEWLINE.join(ptcn[it].text.strip() for it in poc.caption)
        collected.append('TOKENS:\n' + code)
        collected.append('CAPTION:\n' + captio)
    header = f'################################# {pagenr} #################################\n'
    result = header + utilo.NEWLINE.join(collected) + utilo.NEWLINE * 4
    return result
