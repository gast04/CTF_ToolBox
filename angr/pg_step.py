#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 09:56:28 2017

@author: niku
"""

import angr


binary = "/home/niku/git-repos/BacArbeit/Explorer4/testcases/mycrack"

proj = angr.Project(binary)

argv1 = angr.claripy.BVS("input", 8*12)


entry_state = proj.factory.entry_state(args=[binary, argv1])


pg = proj.factory.path_group(entry_state)


pg.



