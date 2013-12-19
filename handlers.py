# -*- coding: utf-8 -*-
# simple patch of scotch-base with the twilio api to respond to 
# texts sent to trial account.  Will be extended to extract report
# information from incoming texts.
#
# @author: Rahul Dhodapkar (krishnakid)
# @version: 12.19.13

import datetime
import webapp2
from webapp2_extras import jinja2
import twilio.twiml

callers = {
    "+13475633757": "Rahul Dhodapkar"
}

class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests all other handlers will
        extend this handler

    """
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template_name, template_values):
        self.response.write(self.jinja2.render_template(
            template_name, **template_values))

    def render_string(self, template_string, template_values):
        self.response.write(self.jinja2.environment.from_string(
            template_string).render(**template_values))


class PageHandler(BaseHandler):
    # root function to display CSV with content dump from the 
    # Google Datastore.
    def root(self):
        now = datetime.datetime.now()
        ten_min_ago = now - datetime.timedelta(minutes=10)
        context = {
            'now': now,
            'ten_min_ago': ten_min_ago
        }
        return self.render_template('pages_test_filters.html', context)

    # function to handle incoming twilio texts.  Will load requisite
    # data to the appropriate Google Datastore
    def report(self):
        number = self.request.get('From')
        if number in callers:
            message = "Hello, " + callers[number]
        else:
            message = "Hello, Monkey"
        resp = twilio.twiml.Response()
        resp.message(message)
        context = {}
        return self.render_string(str(resp), context)


