# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import codero

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = codero.PROCESS

power.setup(codero.ROOT)

RESOURCES = [
    power.MASTER110_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR090_PDF,
    (power.BACHELOR075_PDF, '18,40:65'),
    power.BACHELOR067_PDF,
    power.BACHELOR063_PDF,
    (power.BACHELOR241_PDF, '156,200:240'),
    (power.DISS205_PDF, '130:145'),
]

WORKER = utilatest.worker_count(7, onci=len(RESOURCES))


def extract(resources):
    genex.extract(
        files=resources,
        pdfinfo=False,
        groupme='--border',
        pagenumber=True,
        footnote=True,
        pages=':',
        worker=WORKER,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
