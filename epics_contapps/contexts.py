#!/usr/bin/env python

import itertools
from epics_module import EpicsModule as M

all_modules = [
  M("calc", tag="R3-7-4"),
  M("asyn", tag="R4-38"),
  M("StreamDevice", tag="2.8.13", release="STREAM", git_project="paulscherrerinstitute", debian_deps=["libpcre3-dev"], requires=["calc", "asyn"]),
  M("autosave", tag="R5-10-1"),
  M("alive", tag="R1-2-1"),
  M("lua", tag="R2-1", requires=["asyn"]),
  M("caputrecorder", tag="R1-7-3"),
  M("busy", tag="R1-7-2", requires=["asyn", "autosave", "busy"]),
  M("sncseq", tag="2.2.8", site="www-csr.bessy.de", git_project=None, debian_deps=["re2c"]),
  M("deviocstats", tag="3.1.15", repo="iocStats", add_to_release=["MAKE_TEST_IOC_APP=YES"], requires=["sncseq"]),
  M("modbus", tag="R3-0", requires=["asyn"]),
  M("std", tag="R3-6-1", requires=["sncseq", "asyn"]),
  M("ipac", tag="2.15"),
  M("love", tag="R3-2-7", requires=["asyn", "ipac"]),
  M("motor", tag="R7-2-1", requires=["asyn", "sncseq", "busy"]), # probably needs more care with git submodules... https://github.com/epics-modules/motor
  M("camac", tag="R2-7-2", requires=["std", "motor"]),
  M("dac128V", tag="R2-9", requires=["asyn", "ipac"]),
  M("ip", tag="R2-20-1", requires=["asyn", "ipac", "sncseq"]),
  M("sscan", tag="R2-11-3", requires=["sncseq"]),
  M("mca", tag="R7-8", requires=["calc", "sscan", "busy", "std", "sncseq", "autosave", "asyn", "mca"], debian_deps=["libusb-1.0.0-dev", "libnet1-dev", "libpcap0.8.dev"]),
  M("etherip", tag="ether_ip-3-2", git_project="EPICSTools", repo="ether_ip"),
  M("ip330", tag="R2-9", requires=["asyn", "ipac"]),
  M("ipUnidig", tag="R2-11", requires=["asyn", "ipac"]),
  M("measComp", tag="R2-4", requires=["sncseq", "asyn", "calc", "std", "mca", "busy", "sscan", "autosave", "sncseq", "measComp"], debian_deps=["libhidapi-dev"]),
  M("optics", tag="R2-13-4", requires=["sncseq", "calc", "busy", "asyn"]),
  M("softGlue", tag="R2-8-2", requires=["asyn", "ipac"], add_to_release=["MSI=msi"]),
  M("softGlueZynq", tag="R2-0-2", requires=["asyn", "sncseq", "std"], add_to_release=["MSI=msi"]),
  M("vac", tag="R1-9", requires=["ipac", "asyn"]),
  M("vme", tag="R2-9-2", requires=["sncseq", "std", "asyn"]),
  M("Yokogawa_DAS", tag="R2-0-1", requires=["sncseq"]),
  M("xxx", tag="R6-1"), # optional: requires=["tds3000", "fly"]),
  # currently too much effort to include these, could add later:
  #M("areaDetector", tag="R3-9", git_project="areaDetector"), # -> needs a lot of git submodule stuff... https://areadetector.github.io/master/install_guide.html
  #M("quadEM", tag="R9-3", requires=["quadEM", "ipac", "ipUnidig", "areaDetector"]),
  #M("dxp", tag="R6-0", requires=["dxp", "mca", "sncseq", "areaDetector"]),
  #M("dxpSITORO", tag="R1-2", requires=["sncseq", "mca", "dxpSITORO", "areaDetector"]),
  #M("galil", tag="V3-6", git_project="motorapp", repo="Galil-3-0"), # source is in subdir 3-6
]

def get_module_by_name(name):
    matches = [m for m in all_modules if m.name == name]
    assert len(matches) == 1
    return matches[0]

def get_module_and_requirements(name, gathered_modules=None):
    if gathered_modules is None:
        gathered_modules = []
    this_module = get_module_by_name(name)
    if this_module not in gathered_modules:
        gathered_modules.append(this_module)
        for required_module_name in this_module.requires:
            get_module_and_requirements(required_module_name, gathered_modules)
    return gathered_modules

CONTEXTS = {
  "modbus": {
    "base_img": "pklaus/epics_base:3.15.6_debian",
    "modules": get_module_and_requirements("modbus"),
    "debian_deps": ["calculated below..."],
  },
  "1-0-0": {
    "base_img": "pklaus/epics_base:7.0.4_debian",
    "modules": all_modules,
    "debian_deps": ["calculated below..."],
  },
}

# Automatically put together required debian packages "debian_deps"
for name, context in CONTEXTS.items():
    debian_deps = [m.debian_deps for m in context["modules"]]
    debian_deps = set(itertools.chain(*debian_deps))
    context["debian_deps"] = sorted(list(debian_deps))

# Validate module inter-dependencies for each build context
for name, context in CONTEXTS.items():
    modules = context["modules"]
    for m in modules:
        for req_name in m.requires:
            found = any(req_name == om.name for om in modules)
            if not found:
                raise RuntimeError(f"CONTEXTS[{name}]: module {m.name} requires {req_name} but it's not part of the modules list.")
