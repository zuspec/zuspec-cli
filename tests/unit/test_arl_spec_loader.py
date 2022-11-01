#****************************************************************************
#* test_arl_spec_loader.py
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

import arl_dataclasses
from tests.unit.test_base import TestBase
from zuspec.arl_spec_loader import ArlSpecLoader


class TestArlSpecLoader(TestBase):

    def test_smoke(self):
        self.addFile("design.py", self.justify("""
            import arl_dataclasses as arl

            print("Hello from design.py")

            @arl.component
            class pss_top(object):

                @arl.action
                class MyA(object):
                    pass

                pass

            print("qualname: %s" % pss_top.MyA.__qualname__)
        """))

        loader = ArlSpecLoader()
        loader.addPythonPath(self.testdir)
        loader.addLoadPyModule("design")

        loader.load()

        arl_ctxt = arl_dataclasses.impl.Ctor.inst().ctxt()

        self.assertIsNotNone(arl_ctxt.findDataTypeComponent("pss_top"))
        self.assertIsNotNone(arl_ctxt.findDataTypeAction("pss_top::MyA"))

