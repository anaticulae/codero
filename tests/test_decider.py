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

import codero.strategy.decider


def test_decider_bachelor75all():
    source = power.link(power.BACHELOR075_PDF)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        horizontals=True,
    )
    done = codero.strategy.decider.run(ptcn)
    assert len(done) == 8
