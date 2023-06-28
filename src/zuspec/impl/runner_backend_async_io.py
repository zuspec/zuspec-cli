#****************************************************************************
#* runner_backend_async_io.py
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
import asyncio
from .runner_backend import RunnerBackend

class RunnerBackendAsyncIO(RunnerBackend):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        pass

    def start(self, coro):
        return asyncio.Task(coro, self.loop)
    
    async def join(self, coro):
        yield asyncio.wait_for(coro, None)
    
    def mkEvent(self):
        return asyncio.Event(loop=self.loop)


