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
import utila


def run(strategy, resource, pages: tuple = None, horizontals: bool = False):
    source = power.link(resource)
    ptcn = serializeraw.ptcn_frompath(
        path=source,
        prefix='oneline',
        pages=pages,
        horizontals=horizontals,
    )
    if isinstance(pages, int):
        result = strategy(ptcn[0])
    else:
        result = [strategy(page) for page in ptcn]
    return result


def raw(source, extracted) -> str:
    collected = []
    ptcns = serializeraw.ptcn_frompath(
        source,
        prefix='oneline',
        horizontals=True,
    )
    for page in extracted:
        ptcn = utila.select_page(ptcns, page.page)
        collected.append(rawpage(ptcn, page))
    result = utila.NEWLINE.join(collected)
    return result


def rawpage(ptcn, page) -> str:
    pagenr = page.page
    content = page.content
    collected = []
    for poc in content:
        code = utila.NEWLINE.join(ptcn[it].text.strip() for it in poc.tokens)
        captio = utila.NEWLINE.join(ptcn[it].text.strip() for it in poc.caption)
        collected.append('TOKENS:\n' + code)
        collected.append('CAPTION:\n' + captio)
    header = f'############ {pagenr} ############\n'
    result = header + utila.NEWLINE.join(collected)
    return result
