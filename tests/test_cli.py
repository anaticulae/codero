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
import serializeraw

import tests


def test_nocodes(testdir, monkeypatch):
    source = power.link(power.MASTER110_PDF)
    tests.run(f'-i {source} -o {testdir.tmpdir}', monkeypatch=monkeypatch)
    outpath = os.path.join(testdir.tmpdir, 'codero__text_text.yaml')
    loaded = serializeraw.load_codes(outpath)
    assert not loaded
