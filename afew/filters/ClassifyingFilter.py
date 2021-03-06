# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

#
# Copyright (c) Justus Winter <4winter@informatik.uni-hamburg.de>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import logging

from ..DBACL import DBACL as Classifier, ClassificationError
from .BaseFilter import Filter
from ..utils import extract_mail_body

class ClassifyingFilter(Filter):
    message = 'Tagging via classification'
    def __init__(self, database, *args, **kwargs):
        super(ClassifyingFilter, self).__init__(database, *args, **kwargs)

        self.classifier = Classifier()

    def handle_message(self, message):
        try:
            scores = self.classifier.classify(extract_mail_body(message))
        except ClassificationError as e:
            logging.warning('Classification failed: {}'.format(e))
            return

        category = scores[0][0]

        if category != self.classifier.reference_category:
            self.add_tags(message, category)
