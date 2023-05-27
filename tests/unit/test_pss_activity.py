#****************************************************************************
#* test_pss_activity.py
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
from .test_base import TestBase
from zuspec.arl_spec_loader import ArlSpecLoader
import vsc_solvers.core as vsc_solvers
import zsp_arl_dm.core as arl_dm
import zsp_arl_eval.core as arl_eval
from zuspec.impl.generator_dot import GeneratorDot
import zsp_be_sw.core as be_sw


class TestPssActivity(TestBase):

    def test_smoke(self):
        self.addFile("pss_top.pss", self.justify("""
        component pss_top {
            action A { }
            action B { }
            action Entry {

            }
        }
        """))

        loader = ArlSpecLoader()
        loader.addLoadPss([os.path.join(self.testdir, "pss_top.pss")])

        loader.load()

        arl_eval_f = arl_eval.Factory.inst()
        vsc_solvers_f = vsc_solvers.Factory.inst()
        randstate = vsc_solvers_f.mkRandState("")

        evaluator = arl_eval_f.mkModelEvaluator(
            arl_eval.ModelEvaluatorKind.FullElab,
            vsc_solvers_f,
            loader.ctxt)
        
        pss_top_t = loader.ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top_Entry_t = loader.ctxt.findDataTypeAction("pss_top::Entry")
        self.assertIsNotNone(pss_top_Entry_t)

        build_ctxt = arl_dm.ModelBuildContext(loader.ctxt)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
        pss_top.initCompTree()

        eval_it = evaluator.eval(
            randstate,
            pss_top,
            pss_top_Entry_t)
        self.assertIsNotNone(eval_it)

        gen = GeneratorDot(pss_top)

        dot = gen.gen(eval_it)
        print("Dot:\n%s\n" % dot)

    pass

    def test_smoke_c(self):
        self.addFile("pss_top.pss", self.justify("""
        import addr_reg_pkg::*;

        component pss_top {
            /*
            executor_c<>     e0;
            executor_group_c<>   eg0;

            exec init_down {
                eg0.add_executor(e0);
            }
             */

            action A { }
            action B { }
            action Entry {

            }
        }
        """))

        loader = ArlSpecLoader()
        loader.addLoadPss([os.path.join(self.testdir, "pss_top.pss")])

        loader.load()

        arl_eval_f = arl_eval.Factory.inst()
        vsc_solvers_f = vsc_solvers.Factory.inst()
        randstate = vsc_solvers_f.mkRandState("")

        evaluator = arl_eval_f.mkModelEvaluator(
            arl_eval.ModelEvaluatorKind.FullElab,
            vsc_solvers_f,
            loader.ctxt)
        
        pss_top_t = loader.ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top_Entry_t = loader.ctxt.findDataTypeAction("pss_top::Entry")
        self.assertIsNotNone(pss_top_Entry_t)

        build_ctxt = arl_dm.ModelBuildContext(loader.ctxt)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
        pss_top.initCompTree()

        eval_it = evaluator.eval(
            randstate,
            pss_top,
            pss_top_Entry_t)
        self.assertIsNotNone(eval_it)

        be_sw_f = be_sw.Factory.inst()
        out_h = be_sw_f.mkFileOutput("out.h")
        out_c = be_sw_f.mkFileOutput("out.c")
        testgen = be_sw_f.mkGeneratorMultiCoreSingleImageEmbCTest(
            [],
            -1,
            out_h,
            out_c
        )

        testgen.generate(pss_top, eval_it)
        out_h.close()
        out_c.close()

    def test_multi_level_component(self):
        self.addFile("pss_top.pss", self.justify("""
        import addr_reg_pkg::*;

        component DMA {
            int         base;

            action Mem2Mem { 
                exec body {
                    comp.base = 1;
                }
            }
        }

        component pss_top {
            DMA         dma0;
            DMA         dma1;

            action Entry {
                activity {
                    do DMA::Mem2Mem;
                    do DMA::Mem2Mem;
                    do DMA::Mem2Mem;
                }
            }
        }
        """))

        loader = ArlSpecLoader()
        loader.addLoadPss([os.path.join(self.testdir, "pss_top.pss")])

        loader.load()

        arl_eval_f = arl_eval.Factory.inst()
        vsc_solvers_f = vsc_solvers.Factory.inst()
        randstate = vsc_solvers_f.mkRandState("")

        evaluator = arl_eval_f.mkModelEvaluator(
            arl_eval.ModelEvaluatorKind.FullElab,
            vsc_solvers_f,
            loader.ctxt)
        
        pss_top_t = loader.ctxt.findDataTypeComponent("pss_top")
        self.assertIsNotNone(pss_top_t)
        pss_top_Entry_t = loader.ctxt.findDataTypeAction("pss_top::Entry")
        self.assertIsNotNone(pss_top_Entry_t)

        build_ctxt = arl_dm.ModelBuildContext(loader.ctxt)
        pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
        pss_top.initCompTree()

        eval_it = evaluator.eval(
            randstate,
            pss_top,
            pss_top_Entry_t)
        self.assertIsNotNone(eval_it)

        be_sw_f = be_sw.Factory.inst()
        out_h = be_sw_f.mkFileOutput("out.h")
        out_c = be_sw_f.mkFileOutput("out.c")
        testgen = be_sw_f.mkGeneratorMultiCoreSingleImageEmbCTest(
            [],
            -1,
            out_h,
            out_c
        )

        testgen.generate(pss_top, eval_it)
        out_h.close()
        out_c.close()


