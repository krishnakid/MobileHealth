# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import filters
import webapp2
from webapp2 import Route
from twilio import twiml
from twilio.rest import TwilioRestClient

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# twilio authentication information for account
tw_account_sid = "AC944b22c32e5665d6d2744b131689e964"
tw_auth_token = "df78e3cc5ff61c383d8fe6dbbd0c9b0c"

client = TwilioRestClient(tw_account_sid, tw_auth_token)

routes = [
    Route('/', handler='handlers.PageHandler:root', name='pages-root'),
    Route('/report', handler='handlers.PageHandler:report', name='pages-report'),
    ]

config = {
    'webapp2_extras.jinja2': {
        'template_path': 'template_files',
        'filters': {
            'timesince': filters.timesince,
            'datetimeformat': filters.datetimeformat,
        },
    },
}


application = webapp2.WSGIApplication(routes, debug=DEBUG, config=config)
