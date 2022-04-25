# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.requires(power.BACHELOR111_PDF)
def test_bachelor111p35(testdir, monkeypatch):
    source = power.link(power.BACHELOR111_PDF)
    tests.run(
        f'-i {source} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    loaded = serializeraw.load_codes(testdir.tmpdir)
    page35 = utila.select_page(loaded, page=35)
    assert page35
