# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import codero.decider
import codero.features.horizontal
import codero.features.text


@utilatest.requires(power.BACHELOR075_PDF)
def test_decider_bachelor75all():
    source = power.link(power.BACHELOR075_PDF)
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
