# -*- coding: utf-8 -*-

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
import json
import uuid
from .dict import DictionarySerializer
from ..operators import Attrib
from ..camunda.specs.UserTask import Form

def object_hook(dct):
    if '__uuid__' in dct:
        return uuid.UUID(dct['__uuid__'])

    if '__bytes__' in dct:
        return dct['__bytes__'].encode('ascii')

    if '__attrib__' in dct:
        return Attrib(dct['__attrib__'])

    if '__form__' in dct:
        return Form(init=json.loads(dct['__form__']))


    return dct


def JsonableHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise 'Object of type %s with value of %s is not JSON serializable' % (
            type(Obj), repr(Obj))





def default(obj):
    if isinstance(obj, uuid.UUID):
        return {'__uuid__': obj.hex}

    if isinstance(obj, bytes):
        return {'__bytes__': obj.decode('ascii')}

    if isinstance(obj, Attrib):
        return {'__attrib__': obj.name}

    if isinstance(obj,Form):
        return {'__form__': json.dumps(obj, default=JsonableHandler)}

    raise TypeError('%r is not JSON serializable' % obj)


def loads(text, cls=None):
    return json.loads(text, object_hook=object_hook, cls=cls)


def dumps(dct, cls=None):
    return json.dumps(dct, sort_keys=True, default=default, cls=cls)


class JSONSerializer(DictionarySerializer):

    # used as the cls= parameter to json.dumps and json.loads
    json_serializer_cls = None

    def __init__(self, json_serializer_cls=None, *args, **kwargs):
        if json_serializer_cls:
            self.json_serializer_cls = json_serializer_cls
        super().__init__(*args, **kwargs)
        
    def serialize_workflow_spec(self, wf_spec, **kwargs):
        thedict = super(JSONSerializer, self).serialize_workflow_spec(
            wf_spec, **kwargs)
        return dumps(thedict)

    def deserialize_workflow_spec(self, s_state, **kwargs):
        thedict = loads(s_state, cls=self.json_serializer_cls)
        return super(JSONSerializer, self).deserialize_workflow_spec(
            thedict, **kwargs)

    def serialize_workflow(self, workflow, **kwargs):
        thedict = super(JSONSerializer, self).serialize_workflow(
            workflow, **kwargs)
        return dumps(thedict, cls=self.json_serializer_cls)

    def deserialize_workflow(self, s_state, **kwargs):
        thedict = loads(s_state, cls=self.json_serializer_cls)
        return super(JSONSerializer, self).deserialize_workflow(
            thedict, **kwargs)
