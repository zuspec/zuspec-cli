#****************************************************************************
#* test_activity_bind_explicit.py
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

import vsc_dm.core as vsc_dm
import zsp_arl_dm.core as arl_dm
import zsp_dataclasses
from .test_base import TestBase
from zuspec.impl.generator_dot import GeneratorDot
from zuspec.arl_spec_loader import ArlSpecLoader

class TestActivityBindExplicit(TestBase):

    def test_smoke(self):
        vsc_dm.enableDebug(True)
        self.addFile("pss_top.py", self.justify("""
            import zsp_dataclasses as arl

            @arl.buffer
            class Data(object):
                pass

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    dat_o : arl.output[Data]
                    pass

                @arl.action
                class B(object):
                    dat_i : arl.input[Data]

                    a : arl.rand_uint16_t
                    b : arl.rand_uint16_t
                    c : arl.rand_uint16_t
                    d : arl.rand_uint16_t

                @arl.action
                class Entry(object):
                    a : 'pss_top.A'
                    b : 'pss_top.B'

                    @arl.activity
                    def activity(self):
                        self.a()
                        self.b()

                        arl.bind(self.a.dat_o, self.b.dat_i)
                    pass
        """))

        loader = ArlSpecLoader()
        loader.addPythonPath(self.testdir)
        loader.addLoadPyModule("pss_top")

        loader.load()

        # Create an evaluator
        arl_ctxt = zsp_dataclasses.impl.Ctor.inst().ctxt()

        build_ctxt = arl_dm.ModelBuildContext(arl_ctxt)
        pss_top_t = arl_ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)

        pss_top.initCompTree()

        rs = arl_ctxt.mkRandState("")
        eval = arl_ctxt.mkModelEvaluator()
        eval_it = eval.eval(
            rs.next(),
            pss_top,
            arl_ctxt.findDataTypeAction("pss_top::Entry")
        )

        gen = GeneratorDot(pss_top)

        dot = gen.gen(eval_it)
        print("Dot:\n%s\n" % dot)

