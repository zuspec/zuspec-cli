#****************************************************************************
#* deferred_task_caller.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import zsp_arl_eval.core as zsp_eval

class DeferredTaskCaller(object):

    def __init__(self, thread, func, params, ret_xformer):
        self._thread = thread
        self._func = func
        self._params = params
        self._ret_xformer = ret_xformer
        pass

    async def call(self):
        ret = await self._func(*self._params)
        if self._ret_xformer is not None:
            self._thread.setResult(self._ret_xformer(self._thread, ret))
        else:
            self._thread.setResult(self._thread.mkValRefInt(0, False, 1))



