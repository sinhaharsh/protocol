#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from protocol.base import Unspecified, BaseParameter
from protocol import ImagingSequence
from protocol.imaging import TR, FA, EES, TE, PED

test_dir = Path(__file__).parent.resolve()
# base_dir = test_dir / 'datasets'
# base_dir = Path('/Volumes/work/rotman/BIDS-examples/')
base_dir = Path('/Users/Reddy/Downloads/dicom')
ds_name = 'ABCD'  # 'ds114_test2'
ds_path = base_dir / ds_name


tr = TR(1200)
fa = FA(90)
ees = EES(10)
te = TE(10)
ped = PED('ROW')

seq = ImagingSequence('MRI')
seq.add([tr, fa, te])

s2 = ImagingSequence()
s2.add([fa, tr, ped])

print(s2.compliant(seq))
print(s2==seq)

print('test')
