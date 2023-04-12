#****************************************************************************
#* test_type_extension.py
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

import zsp_dataclasses
import zsp_arl_dm.core as arl_dm
import vsc_dm.core as vsc_dm
import vsc_solvers.core as vsc_solvers

from zuspec.arl_spec_loader import ArlSpecLoader
from zuspec.impl.generator_dot import GeneratorDot
from zuspec.impl.seq_eval_iterator_processor import SeqEvalIteratorProcessor
from .test_base import TestBase

class TestTypeExtension(TestBase):

    def test_smoke(self):
        self.addFile("pss_top.py", self.justify("""
            import zsp_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):

                    @arl.exec.body
                    async def body(self):
                        print("Hello from Body %d %d" % (self.a, self.b))

                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):

                    @arl.activity
                    def activity(self):
                        arl.do[pss_top.A]
                        arl.do[pss_top.B]

            @arl.extend.action(pss_top.A)
            class ext(object):
                a : arl.int16_t = 2

            @arl.extend.action(pss_top.A)
            class ext(object):
                b : arl.int16_t = 3
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

        rs = vsc_solvers.Factory.inst().mkRandState("")
        eval = arl_ctxt.mkModelEvaluator()
        eval_it = eval.eval(
            rs.next(),
            pss_top,
            arl_ctxt.findDataTypeAction("pss_top::Entry")
        )

        eval = SeqEvalIteratorProcessor(pss_top)

        eval.process(eval_it)

    def test_constraint(self):
        self.addFile("pss_top.py", self.justify("""
            import zsp_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    a : arl.rand_uint16_t
                    b : arl.rand_uint16_t

                    @arl.exec.body
                    async def body(self):
                        print("Hello from Body %d %d" % (self.a, self.b))

                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):

                    @arl.activity
                    def activity(self):
                        arl.do[pss_top.A]
                        arl.do[pss_top.B]

            @arl.extend.action(pss_top.A)
            class ext(object):
                @arl.constraint
                def ab_c(self):
                    self.a < self.b

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

        eval = SeqEvalIteratorProcessor(pss_top)

        eval.process(eval_it)

    def test_exec(self):
        self.addFile("pss_top.py", self.justify("""
            import zsp_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    a : arl.rand_uint16_t
                    b : arl.rand_uint16_t


                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):

                    @arl.activity
                    def activity(self):
                        arl.do[pss_top.A]
                        arl.do[pss_top.B]

            @arl.extend.action(pss_top.A)
            class ext(object):
                @arl.constraint
                def ab_c(self):
                    self.a < self.b

                @arl.exec.body
                async def body(self):
                    print("Hello from Body %d %d" % (self.a, self.b))

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

        eval = SeqEvalIteratorProcessor(pss_top)

        eval.process(eval_it)

    def test_activity(self):
        self.addFile("pss_top.py", self.justify("""
            import zsp_dataclasses as arl

            @arl.component
            class pss_top(object):

                @arl.action
                class A(object):
                    a : arl.rand_uint16_t
                    b : arl.rand_uint16_t

                    @arl.constraint
                    def ab_c(self):
                        self.a < self.b

                    @arl.exec.body
                    async def body(self):
                        print("Hello from Body %d %d" % (self.a, self.b))


                @arl.action
                class B(object):
                    pass

                @arl.action
                class Entry(object):
                    pass


            @arl.extend.action(pss_top.Entry)
            class ext(object):
                @arl.activity
                def activity(self):
                    arl.do[pss_top.A]
                    arl.do[pss_top.B]

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

        rs = vsc_solvers.Factory.inst().mkRandState("")
        eval = arl_ctxt.mkModelEvaluator()
        eval_it = eval.eval(
            rs.next(),
            pss_top,
            arl_ctxt.findDataTypeAction("pss_top::Entry")
        )

        eval = SeqEvalIteratorProcessor(pss_top)

        eval.process(eval_it)

    def test_activity_pss(self):
        self.addFile("pss_top.pss", self.justify("""

            component pss_top {

                action A {
                    rand bit[16] a;
                    rand bit[16] b;

                    constraint ab_c {
                        self.a < self.b;
                    }

                    exec body {
                        print("Hello from Body %d %d" % (self.a, self.b));
                    }
                }

                action B { }

                action Entry {
                    do A;
                    do B;
                }
            }

        """))

        loader = ArlSpecLoader()
        loader.addLoadPss(["pss_top.pss"])

        loader.load()

        # Create an evaluator
        arl_ctxt = zsp_dataclasses.impl.Ctor.inst().ctxt()

        build_ctxt = arl_dm.ModelBuildContext(arl_ctxt)
        pss_top_t = arl_ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)

        pss_top.initCompTree()

        rs = vsc_solvers.Factory.inst().mkRandState("")
        eval = arl_ctxt.mkModelEvaluator()
        eval_it = eval.eval(
            rs.next(),
            pss_top,
            arl_ctxt.findDataTypeAction("pss_top::Entry")
        )

        eval = SeqEvalIteratorProcessor(pss_top)

        eval.process(eval_it)