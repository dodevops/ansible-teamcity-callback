# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: teamcity
    type: stdout
    short_description: Ansible output suitable for TeamCity
    version_added: 0.1.0
    description:
        - This plugins reformats the default output of Ansible to be better usable when running playbooks in TeamCity
    extends_documentation_fragment:
      - default_callback
    requirements:
      - set as stdout in configuration
'''

from ansible import constants as C
from ansible.plugins.callback.default import CallbackModule as DefaultModule

class CallbackModule(DefaultModule):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'teamcity'

    def __init__(self):
        self._last_task_block = None
        self._last_play_block = None
        super(CallbackModule, self).__init__()

    # Close the previously opened task block
    def _close_task_block(self):
        if self._last_task_block is not None:
            self._display.display(u"##teamcity[blockClosed name='%s']" % (self._last_task_block))
            self._last_task_block = None

    # Close the previously opened play block
    def _close_play_block(self):
        if self._last_play_block is not None:
            self._display.display(u"##teamcity[blockClosed name='%s']" % (self._last_play_block))
            self._last_play_block = None

    # Open a new task block
    def _print_task_banner(self, task):
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = u', '.join(u'%s=%s' % a for a in task.args.items())
            args = u' %s' % args

        prefix = self._task_type_cache.get(task._uuid, 'TASK')

        # Use cached task name
        task_name = self._last_task_name
        if task_name is None:
            task_name = task.get_name().strip()
       
        self._close_task_block()

        self._display.display(u"##teamcity[blockOpened name='%s [%s]' description='%s']" % (prefix, task_name, args))
        if self._display.verbosity >= 2:
            path = task.get_path()
            if path:
                self._display.display(u"task path: %s" % path, color=C.COLOR_DEBUG)

        self._last_task_block = u"%s [%s]" % (prefix, task_name)  
        self._last_task_banner = task._uuid
    
    # Open a new play block
    def v2_playbook_on_play_start(self, play):

        self._close_task_block()
        self._close_play_block()

        name = play.get_name().strip()
        if not name:
            msg = u"PLAY"
        else:
            msg = u"PLAY [%s]" % name

        self._display.display(u"##teamcity[blockOpened name='%s']" % (msg))
        self._last_play_block = msg
        self._play = play

    # This is the last step, so previously opened tasks and plays should be closed
    def v2_playbook_on_stats(self, stats):
        self._close_task_block()
        self._close_play_block()

        super(CallbackModule, self).v2_playbook_on_stats(stats) 
