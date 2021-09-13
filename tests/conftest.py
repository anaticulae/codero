# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import codero

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = codero.PROCESS
WORKER = 6

power.setup(codero.ROOT)

RESOURCES = [
    (power.BACHELOR075_PDF, '18,40:65'),
    (power.BACHELOR111_PDF, '35,45:66'),
    (power.BACHELOR067_PDF, '10:21,40:65'),
]


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        pdfinfo=False,
        tablero=False,
        rawmaker_cleanup=False,
        groupme=True,
        pages=':',
        worker=WORKER,
        base=power.REPOSITORY,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
