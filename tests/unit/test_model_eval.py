#****************************************************************************
#* test_model_eval.py
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
import os
from unit.test_base import TestBase
from zuspec.arl_spec_loader import ArlSpecLoader
from zuspec.loader import Loader
import vsc_solvers.core as vsc_solvers
import zsp_arl_dm.core as arl_dm
import zsp_arl_eval.core as arl_eval

class TestModelEval(TestBase):

    def test_smoke(self):
        content = """
        function void doit();
        import function doit;

        component pss_top {
            action Entry { 
                exec body {
                    doit();
                }
            }
        }
        """

        self.enableDebug(True)

        loader = Loader()
        ctxt = loader.load(content)

        arl_eval_f = arl_eval.Factory.inst()
        vsc_solvers_f = vsc_solvers.Factory.inst()
        randstate = vsc_solvers_f.mkRandState("")

        pss_top_t = ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top_Entry_t = ctxt.findDataTypeAction("pss_top::Entry")
        self.assertIsNotNone(pss_top_Entry_t)

        build_ctxt = arl_dm.ModelBuildContext(ctxt)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
        pss_top.initCompTree()

        class MyBackend(arl_eval.EvalBackend):

            def enterAction(self, thread, action):
                print("enterAction: %s" % action.name())

            def leaveAction(self, thread, action):
                print("leaveAction: %s" % action.name())

            def callFuncReq(self, thread, func_t, params):
                print("callFuncReq")

        backend = MyBackend()
        evaluator = arl_eval_f.mkEvalContextFullElab(
            vsc_solvers_f,
            ctxt,
            randstate,
            pss_top,
            pss_top_Entry_t,
            backend)
        print("Post-eval-create %d" % len(evaluator.getFunctions()))
        self.assertEqual(len(evaluator.getFunctions()), 13)

        for f in evaluator.getFunctions():
            print("Function: %s" % f.name())

        self.assertTrue(evaluator.eval())

        pass



