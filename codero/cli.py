# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import codero

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'text',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'oneline_fonts_header'),
            utila.ResultFile('rawmaker', 'oneline_fonts_content'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'horizontals_horizontals'),
        ],
        output=('text',),
    ),
]


def main():
    utila.featurepack(
        root=codero.ROOT,
        workplan=WORKPLAN,
        featurepackage='codero.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=codero.PROCESS,
            pages=True,
            version=codero.__version__,
        ),
    )
