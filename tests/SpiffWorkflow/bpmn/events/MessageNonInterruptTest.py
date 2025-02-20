# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division, absolute_import
import unittest
import datetime
import time
from SpiffWorkflow.task import Task
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from tests.SpiffWorkflow.bpmn.BpmnWorkflowTestCase import BpmnWorkflowTestCase

__author__ = 'matth'


class MessageNonInterruptTest(BpmnWorkflowTestCase):

    def setUp(self):
        self.spec = self.load_spec()
        # self.spec.dump()

    def load_spec(self):
        return self.load_workflow_spec('Test-Workflows/*.bpmn20.xml', 'Test Workflows')

    def testRunThroughHappySaveAndRestore(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.save_restore()
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()
        self.save_restore()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.do_next_exclusive_step('Do Something That Takes A Long Time')
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))

        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))

    def testRunThroughMessageInterruptSaveAndRestore(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.save_restore()
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()
        self.save_restore()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.workflow.message('Test Message')
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Acknowledge Non-Interrupt Message')
        self.workflow.do_engine_steps()
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Do Something That Takes A Long Time')
        self.workflow.do_engine_steps()
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))

    def testRunThroughHappy(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.do_next_exclusive_step('Do Something That Takes A Long Time')

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))

    def testRunThroughMessageInterrupt(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.workflow.message('Test Message')

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Acknowledge Non-Interrupt Message')

        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.do_next_named_step('Do Something That Takes A Long Time')

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))

    def testRunThroughMessageInterruptOtherOrder(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.workflow.message('Test Message')

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Do Something That Takes A Long Time')

        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Acknowledge Non-Interrupt Message')

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))

    def testRunThroughMessageInterruptOtherOrderSaveAndRestore(self):

        self.workflow = BpmnWorkflow(self.spec)
        self.save_restore()
        self.do_next_exclusive_step(
            'Select Test', choice='Message Non Interrupt')
        self.workflow.do_engine_steps()
        self.save_restore()

        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.WAITING)))

        self.workflow.message('Test Message')
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(0, len(self.workflow.get_tasks(Task.WAITING)))
        self.assertEqual(2, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Do Something That Takes A Long Time')
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))
        self.assertEqual(1, len(self.workflow.get_tasks(Task.READY)))

        self.do_next_named_step('Acknowledge Non-Interrupt Message')
        self.save_restore()

        self.workflow.do_engine_steps()
        self.assertEqual(
            0, len(self.workflow.get_tasks(Task.READY | Task.WAITING)))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(MessageNonInterruptTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
