# -*- coding: utf-8 -*-
# simple patch of scotch-base with the twilio api to respond to 
# texts sent to trial account.  Will be extended to extract report
# information from incoming texts.
#
# DEVNOTES:
#           - Twilio texts are capped at 160 chars.
#
#           - Additional error checking should be added to report()
#
#           - report() currently only minimally implemented
#
# @author: Rahul Dhodapkar (krishnakid)
# @version: 12.19.13

import datetime
import webapp2
from webapp2_extras import jinja2
import twilio.twiml
from google.appengine.ext import db


######## DEFINE DATA MODEL ############################
class Report(db.Model):
    #r_time = db.DateProperty(required=True)     # time of report 
    
    r_id = db.StringProperty(required=True)     # ID of reporter

    i_id = db.StringProperty(required=True)     # Infection ID.

    i_loc = db.StringProperty(required=True)    # Location ID.

    i_age = db.IntegerProperty()                # Age of infected

    i_sex = db.BooleanProperty()                # 1 for Male, 0 for Female
################################### END ##############

# for scale, incorporate this into the Google Datastore, but mapping
# would remain the same,
#
#   Phone# --> UserID
callers = {
    "+13475633757": "rd389"
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
        # report body MAX length 160 chars.
        body = self.request.get('Body')

        resp = twilio.twiml.Response()       
        if number in callers:       # valid number
            r_id = callers[number]

            i_age = 0
            i_sex = 0
            i_id = ""
            i_loc = ""

            clean = True
            terms = body.split('.')         # split on delimiter
            # process report body
            for term in terms:
                vals = term.split(":")      # split on inner delim
                if vals[0].upper() == "I":
                    i_id = vals[1]
                elif vals[0].upper() == "L":
                    i_loc = vals[1]
                elif vals[0].upper() == "A":
                    i_age = int(vals[1])
                elif vals[0].upper() == "S":
                    i_sex = vals[1]
                else:
                    clean = False
            # use number as report signature automatically
            if clean:
                rep = Report(r_id = r_id, i_id = i_id, i_loc = i_loc)
                rep.put()
                resp.message("Thanks, " + callers[number] + " for your report")
            else:
                resp.message("Malformed report code, try again.")
        else:
            resp.message("You do not have permission to report.  Please contact registration")

        return self.render_string(str(resp), {})


