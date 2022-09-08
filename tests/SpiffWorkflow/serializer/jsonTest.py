# -*- coding: utf-8 -*-

import sys
import unittest
import os
dirname = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dirname, '..', '..', '..'))

import json
from uuid import UUID, uuid4
from SpiffWorkflow.serializer.json import JSONSerializer
from .dictTest import DictionarySerializerTest


class JSONSerializerTest(DictionarySerializerTest):

    def setUp(self):
        super(JSONSerializerTest, self).setUp()
        self.serializer = JSONSerializer()
        self.return_type = str

    def testCustomJsonEncoderCls(self):
        class MyJsonEncoder(json.JSONEncoder):
            def default(self, z):
                if isinstance(z, UUID):
                    return str(z)
                return super().default(z)
        
        # From the PatternTest ancestor
        workflow = self.workflows[0]
        a_task = workflow.spec.task_specs[list(workflow.spec.task_specs)[0]]
        uuid_val = uuid4()
        a_task.data['jsonTest'] = uuid_val

        try:
            val = a_task.serialize(self.serializer)
            self.assertRaises(TypeError, a_task.serialize, self.serializer)
            custom_serializer = JSONSerializer(json_encoder_cls=MyJsonEncoder)
            serialized_dict = a_task.serialize(custom_serializer)
            self.assertEqual(str(uuid_val), serialized_dict['data']['jsonTest'])
        finally:
            a_task.data.pop('jsonTest',None)

        
    def _prepare_result(self, item):
        return json.loads(item)

    def _compare_results(self, item1, item2, exclude_dynamic=False,
                         exclude_items=None):
        if exclude_dynamic:
            exclude_items = ['__uuid__']
        else:
            exclude_items = []
        super(JSONSerializerTest, self)._compare_results(item1, item2,
                                                         exclude_dynamic=exclude_dynamic,
                                                         exclude_items=exclude_items)


def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(JSONSerializerTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
