#****************************************************************************
#* __main__.py
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
import argparse
import pkgutil
import importlib
from . import CmdRegistry

def getparser():
    parser = CmdRegistry.inst().getParser()
    return parser

def main():
    # TODO: Process filelists

    import sys
    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    discovered_plugins = entry_points(group='zuspec.ext')

    for plugin in discovered_plugins:
        plugin.load()

    # # Load extensions
    # for finder, name, ispkg in pkgutil.iter_modules():
    #     if name.startswith("zsp_ext_"):
    #         print("Load extension: %s" % name)
    #         m = importlib.import_module(name)

    parser = getparser()

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
