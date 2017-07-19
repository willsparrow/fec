# -*- coding: utf8 -*-
# Copyright (C) 2017, www.meibailian.com

import uuid
import logging
# Django
from django.utils import timezone
# FEC
from .models import *


logger = logging.getLogger('django')


def generate_so_no():
    logger.debug('generate so_id')
    no = int(timezone.now().strftime('%Y%m%d') + str(uuid.uuid4().fields[-1])[:6])
    return no

