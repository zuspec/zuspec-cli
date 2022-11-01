#****************************************************************************
#* arl_spec_loader.py
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

import libarl.core as libarl
import sys
import importlib
from typing import List

class ArlSpecLoader(object):
    """Loads an ARL specification from a mix of inputs"""

    def __init__(self):
        self._spec_segments = []
#        self._ctxt = libarl.ArlImpl().mkContext()
        self._pythonpath = []
        pass

    def addLoadPyModule(self, module):
        spec = ArlSpecLoader.LoadSegmentPython(self, module)
        self._spec_segments.append(spec)

    def addPythonPath(self, path):
        self._pythonpath.append(path)

    def addLoadPss(self, files : List[str]):
        spec = ArlSpecLoader.LoadSegementPss()
        self._spec_segments.append(spec)

    def load(self):
        import arl_dataclasses

        for s in self._spec_segments:
            s.load()

        arl_dataclasses.impl.Ctor.inst().elab()

    class LoadSegmentPython(object):

        def __init__(self, loader, module):
            self.loader = loader
            self.module = module
            pass

        def load(self):
            from vsc_dataclasses.impl import Ctor 
            orig_path = sys.path.copy()
            orig_ps = Ctor.inst().setTypePS("::")
            try:
                if len(self.loader._pythonpath) > 0:
                    for e in self.loader._pythonpath:
                        sys.path.insert(0, e)

                print("sys.path=%s" % str(sys.path))
                m = importlib.import_module(self.module)
                print("Module: %s" % str(m))
            finally:
                sys.path = orig_path
                Ctor.inst().setTypePS(orig_ps)

            # TODO: after load, need to elaborate any elements that were loaded

            pass

    class LoadSegmentPss(object):

        def __init__(self, loader, files):
            self.loader = loader
            self.files = files.copy()

        def load(self):
            raise NotImplementedError("LoadSegmentPss.load")
            pass




