from basecamp import Basecamp
from cement.core import foundation, controller
from datetime import date
import elementtree.ElementTree as ET

from settings import *

try:
    bc = Basecamp(BASECAMP_API_URL, BASECAMP_API_KEY)
    xml = bc.me()
    me_tree = ET.fromstring(xml)
    me = {}
    me['id'] = me_tree.find('id').text
    me['name'] = "{0} {1}".format(me_tree.find('first-name').text, me_tree.find('last-name').text)
    print("Hi {0}!".format(me['name']))
except:
    print("Can't find ya bro. Check your api key.")
    quit()


class BasecampController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Basecamp cli thingy"

        config_defaults = dict()

        arguments = [
            (['-d', '--description'], dict(action='store', help='Time entry description')),
            (['-t', '--hours'], dict(action='store', help='Time entry hours')),
            (['-p', '--project'], dict(action='store', help='Time entry project')),
            (['-date'], dict(action='store', help='Time entry date')),
        ]

    @controller.expose(help="get a list of projects")
    def projects(self):
        xml = bc.projects()
        projects = ET.fromstring(xml).findall('.//project')

        output = {}
        for project in projects:
            output[project.find("name").text] = project.find("id").text

        for project in sorted(output):
            print("{0}: {1}".format(output[project], project))

    @controller.expose(help="create time entry")
    def time(self):
        if not app.pargs.date:
            app.pargs.date = date.today().strftime("%y-%m-%d")
        if app.pargs.description and app.pargs.hours and app.pargs.project:
            try:
                bc.create_time_entry(app.pargs.description, float(app.pargs.hours), int(me['id']), entry_date=(app.pargs.date or None), project_id=int(app.pargs.project))
            except:
                print(bc.last_error)
        else:
            print('I need a project_id, description and hours (-p=PROJECTID -d="My description" -t=1.0 [-date=2014-01-01])')


class BasecampApp(foundation.CementApp):
    class Meta:
        label = 'basecamp-cli'
        base_controller = BasecampController

# create the app
app = BasecampApp()

try:
    # setup the application
    app.setup()

    # run the application
    app.run()
finally:
    # close the app
    app.close()