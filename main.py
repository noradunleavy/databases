#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2
from models import Item

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ItemHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/welcome.html")
        self.response.write(start_template.render())

    def post(self):
        the_fav_Item = self.request.get('user-fav-1')

        #put into database (optional)
        Item_record = Item(item_name = the_fav_Item)
        Item_record.put()

        #pass to the template via a dictionary
        variable_dict = {'fav_Item_for_view': the_fav_Item}
        end_template = jinja_current_dir.get_template("templates/results.html")
        self.response.write(end_template.render(variable_dict))

class ShowItemHandler(webapp2.RequestHandler):
    def get(self):
        Item_list_template = jinja_current_dir.get_template("templates/Itemlist.html")
        fav_Items = Item.query().order(-Item.item_name).fetch()
        dict_for_template = {'top_fav_Items': fav_Items}
        self.response.write(Item_list_template.render(dict_for_template))

class CommandHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/command.html")
        self.response.write(start_template.render())

class WorkshopHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/workshop.html")
        self.response.write(start_template.render())

class DatabasesHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/data.html")
        self.response.write(start_template.render())


app = webapp2.WSGIApplication([
    ('/', ItemHandler),
    ('/showfavs', ShowItemHandler),
    ('/workshop', WorkshopHandler),
    ('/commandline', CommandHandler),
    ('/databases', DatabasesHandler),
], debug=True)
