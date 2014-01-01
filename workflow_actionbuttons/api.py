from genshi.builder import tag
from genshi.core import Markup
from genshi.template import MarkupTemplate
from trac.ticket.api import TicketSystem
from trac.config import ConfigSection
from trac.core import Component

class WorkflowManager(Component):

    config_section = ConfigSection('ticket-workflow-action-buttons', '')

    @property
    def action_controllers(self):
        return TicketSystem(self.env).action_controllers

    def allowed_actions(self, allowed, req, ticket):
        return [action for action in 
                TicketSystem(self.env).get_available_actions(req, ticket)
                if allowed is None or action in allowed]

    def controllers_for_action(self, req, ticket, action):
        return [controller for controller in self.action_controllers
                if action in [i[1] for i in controller.get_ticket_actions(req, ticket)]]

    def render_action_control(self, req, ticket, action):
        first_label = None
        widgets = []
        hints = []
        for controller in self.controllers_for_action(req, ticket, action):
            print controller, action
            label, widget, hint = controller.render_ticket_action_control(
                req, ticket, action)
            if first_label is None:
                first_label = label
            widgets.append(widget)
            hints.append(hint)
        return first_label, tag(*widgets), (hints and '. '.join(hints) or '')

    _default_icons = {
        "accept": "fa-thumbs-o-up",
        "leave": "fa-comments-o",
        "reassign": "fa-random",
        "reopen": "fa-minus-square-o",
        "resolve": "fa-check-square-o",
        }

    def render_action_button(self, req, ticket, action):
        template = """
              <label class="button" style="%(css)s">
                <input type="hidden" name="action" value="%(action)s" />
                <a %(comment_required)s name="act"><i class='fa %(icon)s'></i> %(title)s</a>
"""
        data = {
            "action": action,
            "css": self.config_section.get("%s.css" % action) or "",
            "comment_required": (self.config_section.get("%s.comment" % action) == "required"
                                 and 'data-comment="required"' or ""),
            "icon": self.config_section.get("%s.icon" % action, self._default_icons.get(action)),
            "title": self.config_section.get("%s.title" % action, action.title()),
            }
        markup = template % data
        
        supplemental_form = ""
        label, widgets, hints = self.render_action_control(req, ticket, action)
        if widgets.children:
            supplemental_form = "<div class='supplemental'><div class='supplemental-form'>%s %s <span class='hint'>%s</span><textarea style='width:95%%' rows='5' name='comment' placeholder='Enter your comment'></textarea><input type='submit' /></div></div>" % (action.title(), str(widgets), hints)
        markup = markup + supplemental_form + "</label>"
        return Markup(markup)
    
