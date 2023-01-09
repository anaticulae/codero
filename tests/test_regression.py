# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.requires(power.BACHELOR111_PDF)
def test_bachelor111p35(td, mp):
    source = power.link(power.BACHELOR111_PDF)
    tests.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )
    loaded = serializeraw.load_codes(td.tmpdir)
    page35 = utila.select_page(loaded, page=35)
    assert page35
