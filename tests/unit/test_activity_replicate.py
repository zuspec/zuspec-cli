#****************************************************************************
#* test_activity_replicate.py
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
import libarl.core as libarl
import libvsc.core as libvsc
from zuspec.arl_spec_loader import ArlSpecLoader
from zuspec.impl.generator_dot import GeneratorDot
from .test_base import TestBase

class TestActivityReplicate(TestBase):

    def test_smoke(self):
        libvsc.enableDebug(True)
        self.addFile("pss_top.py", self.justify("""
            import arl_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    pass

                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):

                    @arl.activity
                    def activity(self):
                        arl.do[pss_top.A]
                        with arl.replicate(5):
                            arl.do[pss_top.A]
                            arl.do[pss_top.B]
        """))

        loader = ArlSpecLoader()
        loader.addPythonPath(self.testdir)
        loader.addLoadPyModule("pss_top")

        loader.load()

        # Create an evaluator
        arl_ctxt = arl_dataclasses.impl.Ctor.inst().ctxt()

        build_ctxt = libarl.ModelBuildContext(arl_ctxt)
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

    def test_parallel(self):
        libvsc.enableDebug(True)
        self.addFile("pss_top.py", self.justify("""
            import arl_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    pass

                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):

                    @arl.activity
                    def activity(self):
                        arl.do[pss_top.A]
                        with arl.parallel:
                            with arl.replicate(5):
                                arl.do[pss_top.A]
                                arl.do[pss_top.B]
        """))

        loader = ArlSpecLoader()
        loader.addPythonPath(self.testdir)
        loader.addLoadPyModule("pss_top")

        loader.load()

        # Create an evaluator
        arl_ctxt = arl_dataclasses.impl.Ctor.inst().ctxt()

        build_ctxt = libarl.ModelBuildContext(arl_ctxt)
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
