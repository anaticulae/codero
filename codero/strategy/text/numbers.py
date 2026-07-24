# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import configos
import elementae
import iamraw
import utilo

import codero.loc


def linenumbers_and_caption(ptn):
    code = []
    collector = DetectorLineNumbers()
    for index, line in enumerate(ptn):
        done = collector.run(line.text, index)
        if not done:
            continue
        # detected
        code.append(done)
        collector.reset()
    content = [
        iamraw.PeaceOfCode(
            caption=set(utilo.rtuple(done[1], done[2])),
            tokens=set(utilo.rtuple(done[0], done[1])),
        ) for done in code
    ]
    return content


def code_without_caption(ptn):
    code = []
    collector = CodeWithoutCaption()
    for index, line in enumerate(ptn):
        done = collector.run(line.text, index)
        if not done:
            continue
        # detected
        code.append(done)
    final = collector.final()
    if final[0] is not None and final[1] is not None:
        code.append(final)
    content = [
        iamraw.PeaceOfCode(
            caption=set(),
            tokens=set(utilo.rtuple(done[0], done[1])),
        ) for done in code
    ]
    return content


class DetectorLineNumbers:
    """\
    1 $ ./spark-shell
    2 [...]
    3 / __/__ ___ _____/ /__

    Listing 2.1: Word Count in der Spark Konsole

    >>> dtn = DetectorLineNumbers()
    >>> dtn.run('1 import collections', 10)
    >>> dtn.run('2 Abc = collections.namedtuple("Abc a b c")', 11)
    >>> dtn.run('Listing 3: Simple python example', 12)
    (10, 12, 13)
    """

    def __init__(self):
        self.start: int = None
        self.middle: int = None
        self.end: int = None

    def run(self, line: str, index: int):
        text = line.strip()
        if self.start is None:
            if self.loc(text):
                self.start = index
            return None
        if self.loc(text):
            self.middle = index + 1
            return None
        if self.valid(text):
            self.middle = index
            self.end = index + 1
        else:
            self.reset()
            return None
        return self.final()

    def loc(self, text: str) -> bool:  # pylint:disable=R0201
        """Determine if text can be a line of code."""
        return CODE_NUMBER.search(text)

    def valid(self, text: str) -> bool:  # pylint:disable=R0201
        return elementae.iscaption_code(text)

    def final(self):
        result = self.start, self.middle, self.end
        self.reset()
        return result

    def reset(self):
        self.start, self.middle, self.end = None, None, None


CWC_CODE_LENGTH_MIN = configos.HV_INT_PLUS(default=2)


class CodeWithoutCaption(DetectorLineNumbers):
    """\
    Code inside text
    >>> cwc = CodeWithoutCaption()
    >>> cwc.run('Text text text.', 9)
    >>> cwc.run('1 import collections', 10)
    >>> cwc.run('2 Abc = collections.namedtuple("Abc a b c")', 11)
    >>> cwc.run('3 print("hello")', 12)
    >>> cwc.run('Ich bin kein Quellcode.', 13)
    (10, 13)

    Normal List
    >>> cwc = CodeWithoutCaption()
    >>> cwc.run('1. Ich bin ein Listenpunkt', 3)
    >>> cwc.run('2. Haus', 4)
    >>> cwc.run('3. Hund', 5)
    >>> cwc.run('Ich bin kein Quellcode.', 6)

    TODO: ADD OPTION TO HAVE SOME LINES FALSE DETECTION
    """

    def __init__(self):
        super().__init__()
        self.empty_line_count = 0

    def loc(self, text: str) -> bool:
        """\
        Bash Code
        >>> cwc = CodeWithoutCaption()
        >>> cwc.loc('1 #/bin/bash')
        True
        """
        if not CODE_NUMBER.search(text):
            return False
        without_number = CODE_NUMBER.sub('', text).strip()
        if not without_number:
            self.empty_line_count += 1
            return True
        if not codero.loc.determine(without_number):
            return False
        return True

    def valid(self, text: str) -> bool:
        if elementae.iscaption_code(text):
            # see DetectorLineNumbers
            self.reset()
            return False
        if self.middle is None:
            self.reset()
            return False
        length = self.middle - self.start
        if length < CWC_CODE_LENGTH_MIN:
            self.reset()
            return False
        empty_rate = self.empty_line_count / length
        if empty_rate > 0.34:  # TODO: HOLY VALUE
            # skip too many empty lines which are false positive dectections
            self.reset()
            return False
        return True

    def reset(self):
        super().reset()
        self.empty_line_count = 0

    def final(self):
        result = self.start, self.middle
        self.reset()
        return result


CODE_NUMBER = re.compile(r'^\d{1,3}([ ]|(?!\.))')
