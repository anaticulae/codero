# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import codero

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = codero.PROCESS

hoverpower.setup(codero.ROOT)

RESOURCES = [
    hoverpower.MASTER110_PDF,
    hoverpower.BACHELOR111_PDF,
    hoverpower.BACHELOR090_PDF,
    (hoverpower.BACHELOR075_PDF, '18,40:65'),
    hoverpower.BACHELOR067_PDF,
    hoverpower.BACHELOR063_PDF,
    (hoverpower.BACHELOR241_PDF, '156,200:240'),
    (hoverpower.DISS205_PDF, '130:145'),
]

WORKER = utilotest.worker_count(7, onci=len(RESOURCES))


def extract(resources):
    gennex.extract(
        files=resources,
        cleanup=True,
        footnote=True,
        groupme='--border --hefopa',
        headnote=True,
        pagenumber=True,
        pdflog=False,
        pages=':',
        worker=WORKER,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()
