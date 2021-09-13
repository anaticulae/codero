# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex

import codero.strategy.lines
import codero.strategy.text

STRATEGIES = [
    codero.strategy.lines.parse,
    codero.strategy.text.parse,
]


def run(navigators: texmex.PageTextContentNavigators):
    work = [[strategy(page) for page in navigators] for strategy in STRATEGIES]
    # remove empty page parsing
    noempty = [[page for page in result if page.content] for result in work]
    best = decide(noempty)
    return best


def decide(results):
    best = results[0]
    for item in results[1:]:
        if judge(item) > judge(best):
            best = item
    return best


def judge(result) -> int:
    count = 0
    for item in result:
        count += len(item.content)
    return count
