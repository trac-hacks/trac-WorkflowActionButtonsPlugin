from pkg_resources import resource_filename
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import ITemplateProvider
from trac.web.chrome import add_stylesheet, add_script, add_script_data
from trac.core import *

from workflow_actionbuttons.api import WorkflowManager

class WebUI(Component):
    implements(ITemplateStreamFilter, ITemplateProvider)

    # ITemplateProvider methods
    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        return [
            ('workflow_actionbuttons', resource_filename(__name__, 'htdocs/main')),
            ('fontawesome', resource_filename(__name__, 'htdocs/fontawesome')),
            ('jquery.modal', resource_filename(__name__, 'htdocs/jquery.modal')),
            ]

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'ticket.html' and data.get("ticket") and data['ticket'].id:
            add_stylesheet(req, "jquery.modal/jquery.modal.css")
            add_script(req, "jquery.modal/jquery.modal.min.js")

            add_stylesheet(req, "workflow_actionbuttons/actionbuttons.css")
            add_script(req, "workflow_actionbuttons/actionbuttons.js")
            add_stylesheet(req, "fontawesome/css/font-awesome.css")

            manager = WorkflowManager(self.env)
            actions =  manager.allowed_actions(None, req, data['ticket'])

            buttons = []
            for action in actions:
                buttons.append(manager.render_action_button(req, data['ticket'], action))

            add_script_data(req, {"WorkflowActionButtonsPlugin": {
                        'action_buttons': buttons,
                        }})
        return stream
