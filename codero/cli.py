# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import codero

DESCRIPTION = 'TODO'

SOURCES = [
    utilo.ResultFile('rawmaker', 'oneline_text_text'),
    utilo.ResultFile('rawmaker', 'oneline_text_positions'),
    utilo.ResultFile('rawmaker', 'oneline_fonts_header'),
    utilo.ResultFile('rawmaker', 'oneline_fonts_content'),
    utilo.ResultFile('rawmaker', 'border_pages'),
    utilo.ResultFile('groupme', 'footer_footerheader'),
    utilo.ResultFile('rawmaker', 'horizontals_horizontals'),
]

WORKPLAN = [
    utilo.create_step(
        'horizontal',
        inputs=SOURCES,
        output=('horizontal',),
    ),
    utilo.create_step(
        'text',
        inputs=SOURCES,
        output=('text',),
    ),
    utilo.create_step(
        'result',
        inputs=[
            utilo.ResultFile('codero', 'horizontal_horizontal'),
            utilo.ResultFile('codero', 'text_text'),
        ],
        output=('result',),
    ),
]


def main():
    utilo.featurepack(
        root=codero.ROOT,
        workplan=WORKPLAN,
        featurepackage='codero.features',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=codero.PROCESS,
            pages=True,
            version=codero.__version__,
        ),
    )
