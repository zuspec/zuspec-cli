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
from .impl.deferred_task_caller import DeferredTaskCaller
from .impl.function_impl_trap import FunctionImplTrap
from .impl.runner_thread import RunnerThread
from .impl.task_caller import TaskCaller
from .impl.task_build_task_caller import TaskBuildTaskCaller
import asyncio
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
        self._thread_data = []
        self._active_coroutines = []

        self._pss_top_t = self._ctxt.findDataTypeComponent(root_comp)
        if self._pss_top_t is None:
            raise Exception("Failed to find root component type \"%s\"" % root_comp)
        
#        build_ctxt = arl_dm.ModelBuildContext(self._ctxt)
#        self.pss_top = pss_top_t.mkRootField(build_ctxt, "pss_top", False)
#        self.pss_top.initCompTree()
        
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
            self._pss_top_t,
            root_action_t,
            self)

        self.map_functions(evaluator)

        while evaluator.eval():
            if len(self._active_coroutines) == 0:
                if evaluator.eval():
                    raise Exception("stall during execution")
            else:
                await self._backend.joinAny(self._active_coroutines)

                tmp = self._active_coroutines.copy()
                self._active_coroutines.clear()
                for t in tmp:
                    if not self._backend.taskIsDone(t):
                        print("Coroutine not yet done", flush=True)
                        self._active_coroutines.append(t)
                    else:
                        print("Coroutine is done", flush=True)

        if len(self._active_coroutines) > 0:
            raise Exception("runner ending with active coroutines")
        

    def map_functions(self, evaluator):
        if self._executor_if is None:
            self._executor_func_m[None] = {}
            func_m = self._executor_func_m[None]
            for solve in [True, False]:
                functions = evaluator.getSolveFunctions() if solve else evaluator.getTargetFunctions()
                for f in functions:
                    print("Function: %s" % f.name())
                    names = [f.name()]
                    if f.name().find("::") != -1:
                        names.append(f.name().replace(':','_'))
                        names.append(f.name()[f.name().rfind("::")+2:])
                    for name in names:
                        caller_f = inspect.currentframe().f_back

                        while caller_f is not None:
                            if name in caller_f.f_locals.keys():
                                self._executor_func_m[None]
                                # TODO: should probably check args
                                print("Found in locals")
                                assoc_data = TaskBuildTaskCaller().build(
                                    f, 
                                    solve,
                                    caller_f.f_locals[name])
                                f.setAssociatedData(assoc_data)
                                break
                            elif name in caller_f.f_globals.keys():
                                print("Found in globals")
                                assoc_data = TaskBuildTaskCaller().build(
                                    f, 
                                    solve,
                                    caller_f.f_globals[name])
                                f.setAssociatedData(assoc_data)
                                break
                            caller_f = caller_f.f_back
                        if f.getAssociatedData() is not None:
                            break

                    if f.getAssociatedData() is None:
                        # Add a trap function
                        assoc_data = FunctionImplTrap(f, solve)
                        f.setAssociatedData(assoc_data)
        else:
            print("TODO: search executors")

    def enterThreads(self, threads):
        print("enterThreads")

    def leaveThreads(self, threads):
        print("leaveThreads")

    def enterThread(self, thread):
        print("enterThread")
        pass

    def leaveThread(self, thread):
        print("leaveThread")
        pass

    def enterAction(self, thread, action):
        print("enterAction: %s" % action.name())

    def leaveAction(self, thread, action):
        print("leaveAction: %s" % action.name())

    def callFuncReq(self, thread, func_t, params):
        print("callFuncReq")
        task_caller = func_t.getAssociatedData()

        if task_caller is not None:
            print("Invoking the function")
            if task_caller._is_async:
                self._active_coroutines.append(
                    self._backend.start(
                        task_caller.call_target(thread, params)))
            else:
                task_caller.call(thread, params)
        else:
            print("No task caller for %s" % func_t.name())


