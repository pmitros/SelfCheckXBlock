"""OLI-style self-check XBlock."""

import yaml

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


class SelfCheckXBlock(XBlock):
    """
    OLI-style self-check XBlock
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    student_input = String(
        default="", 
        scope=Scope.user_state,
        help="Student submission",
    )

    placeholder = String(
        default = "", 
        scope=Scope.settings, 
        help="placeholder"
    )

    prompt = String(
        default = "", 
        scope=Scope.settings, 
        help="prompt"
    )

    solution = String(
        default = "", 
        scope=Scope.settings, 
        help="solution"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the SelfCheckXBlock, shown to students
        when viewing courses.
        """
        attributes = ""
        html = self.resource_string("static/html/selfcheck.html")
        frag = Fragment(html.format(prompt = self.prompt, 
                                    student_input = self.student_input, 
                                    placeholder = self.placeholder, 
                                    solution = self.solution, 
                                    attributes = attributes
                                    ))
        frag.add_css(self.resource_string("static/css/selfcheck.css"))
        frag.add_javascript(self.resource_string("static/js/src/selfcheck.js"))
        frag.initialize_js('SelfCheckXBlock')
        return frag

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        ''' Parsing XML 
        '''
        block = runtime.construct_xblock_from_class(cls, keys)
        config = yaml.load(node.text)
        block.placeholder = config['Placeholder']
        block.prompt = config['Prompt']
        block.solution = config['Solution']
        return block
 
    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def student_submit(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        self.student_input = data['input']
        return {"success":True}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SelfCheckXBlock",
             """<vertical_demo>
<selfcheck>
Prompt: Can you conclude that the pamphlets are well-matched to the patients reading levels? Look carefully at the data. 
Placeholder: This one demonstrates a Dweck-style mindset intervention
Solution: Nope. And you're an idiot if you thought otherwise. 
</selfcheck>
<selfcheck>
Prompt: A pinch-hitter hits a foul ball which is caught by the right field. What is the direction of the force on the ball in-flight? 
Placeholder: Here is where the student writes her short answer. Example of a culturally-neutral assessment
Solution: Down, and constant. 
</selfcheck>
                </vertical_demo>
             """),
        ]
