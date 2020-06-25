#!/usr/bin/env python

"""
This Python script assembles a Dockerfile to compile EPICS modules
"""

import attr
import typing
import os

# define a generic type for EpicsModule so that we can refer to it while still defining it:
T_EpicsModule = typing.TypeVar('T_EpicsModule', bound='EpicsModule')

@attr.s(auto_attribs=True)
class EpicsModule():
    name: str = ""
    repo: str = None
    release: str = None # the name the module is referred to in configure/RELEASE files
    site: str = "github.com"
    git_project: str = "epics-modules"
    tag: str = ""
    debian_deps: typing.List[str] = attr.Factory(list)
    folder_base: str = ""
    folder_with_tag: bool = True
    requires: typing.List[str] = attr.Factory(list)
    add_to_release: typing.List[str] = attr.Factory(list)

    @property
    def derive_release_name(self):
        return self.release if self.release else self.name.upper()

    @property
    def derive_tarball_name(self):
        return os.path.basename(self.derive_tarball_url)

    @property
    def derive_tarball_url(self):
        if self.site == "github.com":
            return f"https://github.com/{self.git_project}/{self.derive_repository_name}/archive/{self.tag}.tar.gz"
        if self.site == "www-csr.bessy.de":
            return f"https://www-csr.bessy.de/control/SoftDist/sequencer/releases/seq-{self.tag}.tar.gz"
        else:
            raise NotImplementedError(self.git_site)

    @property
    def derive_repository_name(self):
        # use self.repo if defined, otherwise self.name
        return self.repo or self.name

    @property
    def derive_module_folder(self):
        if self.folder_with_tag:
            return f"{self.folder_base or self.name}-{self.tag.replace('.', '-')}"
        else:
            return f"{self.folder_base or self.name}"

    def required_modules(self, available: typing.List[T_EpicsModule]) -> T_EpicsModule:
        for req_name in self.requires:
            matches = [m for m in available if m.name == req_name]
            if len(matches) != 1:
                raise RuntimeError(f"requirement {req_name} has no unique entry in the provided list of available modules")
            yield matches[0]
