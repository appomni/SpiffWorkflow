# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import unittest
from unittest import skip

from SpiffWorkflow.exceptions import WorkflowTaskExecException
from SpiffWorkflow.task import Task
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'matth'


class InlineScriptTest(BpmnWorkflowTestCase):

    def setUp(self):
        self.spec = self.load_spec()

    def load_spec(self):
        return self.load_workflow_spec('ScriptTest.bpmn', 'ScriptTest')

    def testRunThroughHappy(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.workflow.do_engine_steps()
        data = self.workflow.last_task.data
        self.assertEqual(data,{'testvar': {'a': 1, 'b': 2, 'new': 'Test'},
                               'testvar2': [{'x': 1, 'y': 'a'},
                                            {'x': 2, 'y': 'b'},
                                            {'x': 3, 'y': 'c'}],
                               'sample': ['b', 'c']})

    @skip
    def testNoDataPollution(self):
        """Ran into an issue where data from one run of a workflow could
        bleed into a seperate execution.  It will think a variable is there
        when it should not be there"""
        self.workflow = BpmnWorkflow(self.spec)
        startTask = self.workflow.get_tasks(Task.READY)[0]
        self.workflow.do_engine_steps()
        self.assertTrue(self.workflow.is_completed())
        self.assertTrue("testvar" in self.workflow.last_task.data)
        self.assertFalse("testvar" in startTask.data)

        # StartTask doesn't know about testvar, it happened earlier.
        # calling an exec that references testvar, in the context of the
        # start task should fail.
        with self.assertRaises(WorkflowTaskExecException):
            result = self.workflow.script_engine.evaluate(startTask, 'testvar == True')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(InlineScriptTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
