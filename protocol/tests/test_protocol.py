#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from protocol.base import Unspecified, BaseParameter, ImagingSequence
from protocol.imaging import TR, FA

test_dir = Path(__file__).parent.resolve()
base_dir = test_dir / 'datasets'
path_d14 = base_dir / 'ds114_test2'


tr = TR(1200)
fa = FA(90)


seq = ImagingSequence('MRI')
seq.add([tr, fa])

s2 = ImagingSequence()
s2.add([fa, tr])

print(s2.compliant(seq))

print(s2==seq)

print('test')
