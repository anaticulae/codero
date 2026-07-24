# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import codero.decider
import codero.features.horizontal
import codero.features.text


@utilotest.requires(hoverpower.BACHELOR075_PDF)
def test_decider_bachelor75all():
    source = hoverpower.link(hoverpower.BACHELOR075_PDF)
    ptcns = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        horizontals=True,
    )
    done = (
        codero.features.horizontal.run(ptcns),
        codero.features.text.run(ptcns),
    )
    done: list = codero.decider.decide(*done)
    assert len(done) == 8
