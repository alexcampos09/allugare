#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Secret values, sourced from the environment.

Never hardcode credentials here. Set these via environment variables (see
``.env.example`` at the repo root). Empty fallbacks keep imports working in
contexts where a given secret is not needed.
"""

import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
