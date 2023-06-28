#****************************************************************************
#* runner.py
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
from .impl.ctxt import Ctxt
from .impl.runner_thread import RunnerThread
from .impl.task_caller import TaskCaller
import inspect
import vsc_solvers.core as vsc_solvers
import zsp_arl_dm.core as arl_dm
import zsp_arl_eval.core as arl_eval

class Runner(arl_eval.EvalBackend):

    def __init__(
            self, 
            root_comp,
            executor_if=None,
            ctxt=None,
            backend=None):
        super().__init__()
        
        if ctxt is None:
            ctxt = Ctxt.inst().ctxt

        if backend is None:
            backend = Ctxt.inst().backend

            if backend is None:
                raise Exception("No default backend is present")

        self._ctxt = ctxt
        self._backend = backend
        self._executor_if = executor_if
        self._executor_func_m = {}

        pss_top_t = self._ctxt.findDataTypeComponent(root_comp)
        if pss_top_t is None:
            raise Exception("Failed to find root component type \"%s\"" % root_comp)
        
        build_ctxt = arl_dm.ModelBuildContext(self._ctxt)
        self.pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
        self.pss_top.initCompTree()
        
        pass

    async def run(self, root_action, seed=None):
        if seed is not None:
            randstate = vsc_solvers_f.mkRandState(str(seed))
        else:
            randstate = Ctxt.inst().nextState()
            
        arl_eval_f = arl_eval.Factory.inst()
        vsc_solvers_f = vsc_solvers.Factory.inst()

        root_action_t = self._ctxt.findDataTypeAction(root_action)

        if root_action_t == None:
            raise Exception("Failed to find action type %s" % root_action)

        evaluator = arl_eval_f.mkEvalContextFullElab(
            vsc_solvers_f,
            self._ctxt,
            randstate,
            self.pss_top,
            root_action_t,
            self)

        if self._executor_if is None:
            self._executor_func_m[None] = {}
            func_m = self._executor_func_m[None]
            for f in evaluator.getFunctions():
                print("Function: %s" % f.name())
                caller_f = inspect.currentframe().f_back

                while caller_f is not None:
                    if f.name() in caller_f.f_locals.keys():
                        self._executor_func_m[None]
                        # TODO: should probably check args
                        print("Found in locals")
                        func_m[f.name()] = caller_f.f_locals[f.name()]
                    elif f.name() in caller_f.f_globals.keys():
                        print("Found in globals")
                    caller_f = caller_f.f_back
        else:
            print("TODO: search executors")

        while evaluator.eval():
            print("Await")
            break

    def enterThreads(self, threads):
        print("enterThreads")

    def leaveThreads(self, threads):
        print("leaveThreads")

    def enterThread(self, thread):
        print("enterThread")

        if thread.getThreadId() is None:
            print("TODO: Add thread data")
            thread.setThreadId(RunnerThread(self._backend))

    def leaveThread(self, thread):
        print("leaveThread")

    def enterAction(self, thread, action):
        print("enterAction: %s" % action.name())

    def leaveAction(self, thread, action):
        print("leaveAction: %s" % action.name())

    def callFuncReq(self, thread, func_t, params):
        print("callFuncReq")
        task_caller = func_t.getAssociatedData()

        if task_caller is not None:
            task_caller.call(thread, params)
            print("Invoking the function")
        else:
            print("No task caller")


