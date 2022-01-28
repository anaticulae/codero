# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila


def determine(text: str) -> bool:
    """\
    >>> determine('print("hello")')
    True
    """
    text = text.lower().strip()
    methods = [
        isjs,
        ispython,
    ]
    if any(method(text) for method in methods):
        return True
    return False


def prepare(keys, left=r'\b', right=r'\b', escape: bool = False):
    if escape:
        keys = (re.escape(item) for item in keys)
    items = [left + item + right for item in keys]
    result = utila.compiles('(' + '|'.join(items) + ')')
    return result


PYTHON_KEYWORDS = utila.splititems("""assert async await break continue
del elif else except finally for global if lambda pass raise nonlocal
return try while yield yield from as with import""")
PYTHON_KEYWORDS = prepare(PYTHON_KEYWORDS)
PYTHON_METHODS = utila.splititems("""
__import__ abs all any bin bool bytearray bytes chr classmethod compile
complex delattr dict dir divmod enumerate eval filter float format
frozenset getattr globals hasattr hash hex id input int isinstance
issubclass iter len list locals map max memoryview min next object oct
open ord pow print property range repr reversed round set setattr slice
sorted staticmethod str sum super tuple namedtuple
""")
PYTHON_METHODS = prepare(PYTHON_METHODS, right='\\(')


def ispython(text: str) -> bool:
    """\
    >>> ispython('Abc = collections.namedtuple("Abc a b c")')
    True
    """
    if PYTHON_KEYWORDS.search(text):
        return True
    if PYTHON_METHODS.search(text):
        return True
    return False


JAVASCRIPT_KEYWORDS = utila.splitlines("""for own in of while until loop
break return continue switch when then if unless else throw try catch
finally new delete typeof instanceof super true false yes no on off null
NaN Infinity undefined void val map apply length split sum""")
JAVASCRIPT_KEYWORDS = prepare(JAVASCRIPT_KEYWORDS)
# .reduce(
JAVASCRIPT_METHODS = utila.compiles(r'\.[a-z]{3,15}\(')
JAVASCRIPT_START = utila.splititems("""// /** /* * ) } )} val""")
JAVASCRIPT_START = prepare(
    keys=JAVASCRIPT_START,
    left=r'^',
    right='',
    escape=True,
)


def isjs(text: str) -> bool:
    """\
    >>> isjs('.reduce((vector1, vector2) =>')
    True
    >>> isjs('}')
    True
    """
    if JAVASCRIPT_KEYWORDS.search(text):
        return True
    if JAVASCRIPT_METHODS.search(text):
        return True
    if JAVASCRIPT_START.search(text):
        return True
    return False
