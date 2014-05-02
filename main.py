from basecamp import Basecamp
from cement.core import foundation, controller
from datetime import date
import json
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
            (['-m', '--message'], dict(action='store', help='Time entry message')),
            (['-t', '--hours'], dict(action='store', help='Time entry hours')),
            (['-p', '--project'], dict(action='store', help='Time entry project')),
            (['-d', '--date'], dict(action='store', help='Time entry date')),
            (['-n', '--project-name'], dict(action='store', help='Time entry project by name')),
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

        # Save the list of projects to file
        with open('projects.json', 'w') as project_file:
            json.dump(output, project_file)

    @controller.expose(help="create time entry")
    def time(self):
        if app.pargs.project_name:
            project = self.project_name(app.pargs.project_name)
            if len(project) == 1:
                app.pargs.project = project.values()[0]
            elif len(project) > 1:
                print('Too many projects found for the project "{}": {}'.format(app.pargs.project_name, ', '.join(project.keys())))
            else:
                print('No projects found for "{}"'.format(app.pargs.project_name))
        if not app.pargs.date:
            app.pargs.date = date.today().strftime("%Y-%m-%d")
        if app.pargs.message and app.pargs.hours and app.pargs.project:
            try:
                bc.create_time_entry(app.pargs.message, float(app.pargs.hours), int(me['id']), entry_date=(app.pargs.date or None), project_id=int(app.pargs.project))
                print('{} hours added to {} on {}'.format(app.pargs.hours, app.pargs.project, app.pargs.date))
            except:
                print(bc.last_error)
        else:
            print('Hey! I need a project_id, message and hours. (-p=PROJECTID -m="My message" -t=1.0 [-d=2014-01-01])')

    def project_name(self, name):
        "Lookup a project id by it's name"
        name = name.lower()
        try:
            with open('projects.json') as project_file:
                project_names = json.load(project_file)
        except IOError:
            print('No projects saved yet. Run projects command first')
            return {}

        matches = {}
        for project_name in project_names:
            if name in project_name.lower():
                matches[project_name] = project_names[project_name]

        return matches


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
