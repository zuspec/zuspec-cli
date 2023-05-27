#****************************************************************************
#* test_py_user_api.py
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

from .test_base import TestBase
import zuspec
import vsc_solvers.core as vsc_solvers

class TestPyUserApi(TestBase):

    def test_smoke(self):
        self.enableDebug(True)
        ctxt = zuspec.loadContextFromPSS("""
        component pss_top {
          action A { }
        }
        """)

        self.assertIsNotNone(ctxt)
        pss_top_t = ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)

        randstate = vsc_solvers.Factory.inst().mkRandState("0")

        it = zuspec.mkSingleExecutorEvalActionIter(
            ctxt,
            randstate,
            "pss_top",
            "pss_top::A"
        )

    def test_dotgen(self):
        self.enableDebug(False)
        ctxt = zuspec.loadContextFromPSS("""
        component pss_top {
          action A { }
          action B { }
          action Entry {
            activity {
                do A;
                do B;
            }
          }
        }
        """)

        self.assertIsNotNone(ctxt)
        pss_top_t = ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)

        randstate = vsc_solvers.Factory.inst().mkRandState("0")

        graph = zuspec.mkDotGraph(
            ctxt,
            randstate,
            "pss_top",
            "pss_top::Entry"
        )

        print("Graph:\n%s\n" % graph)
        pass

