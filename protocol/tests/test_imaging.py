# test parser of ReceiveCoilActiveElements
from protocol.imaging import ReceiveCoilActiveElements

def test_compare_coil_names():
    value1 = 'HEA;HEP'
    value2 = 'HEP;HEA'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 == rcae2

    value1 = 'BO1,2;BO1-3;SP2-5'
    value2 = 'BO1,2;BO3;SP4,5'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 != rcae2

    value1 = 'BO1,2;BO1-3;SP2-5'
    value2 = 'BO1,2;BO1-3;SP2-5'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 == rcae2

    value1 = 'HC1-7;SP2-5'
    value2 = 'HC1-7;NC1,2'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 == rcae2

    value1 = 'HC1-7'
    value2 = 'HC1-7;NC1,2'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 == rcae2

    value1 = 'HC1,3-7'
    value2 = 'HC1-7;NC1,2'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 != rcae2

    value1 = 'HC1,3'
    value2 = 'HC1-3;NC1,2'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 != rcae2

    value1 = 'HC1-3'
    value2 = 'HC1,3'
    rcae1 = ReceiveCoilActiveElements(value1)
    rcae2 = ReceiveCoilActiveElements(value2)
    assert rcae1 != rcae2


def test_parse_receive_coil_active_elements():
    value = 'HEA;HEP'
    rcae = ReceiveCoilActiveElements(value)
    assert str(rcae) == 'RCAE(HEA;HEP)'
    assert rcae.get_value() == {'HEA': [], 'HEP': []}

    possible_coil_names = ['15K',
                                'BC',
                                'BO1,2;BO1-3;SP2-5',
                                'BO1,2;BO3;SP4,5',
                                'BO1,2;SP2,3',
                                'BO1-3;BO1-3;SP2-6',
                                'BO1-3;BO1-3;SP3-5',
                                'BO1-3;BO1-3;SP3-6',
                                'BO1-3;BO1;SP4-6',
                                'BO1-3;SP2,3',
                                'BO1-3;SP2-4',
                                'BO1-3;SP3,4',
                                'BO2,3;SP2-4',
                                'BO3;BO1-3;SP5-7',
                                'BP1,2;BP1,2;BP1,2;SP4-6',
                                'BP1,2;BP1,2;BP1,2;SP5-7',
                                'BP1,2;BP1,2;BP1;SP3-5',
                                'BP1,2;BP1,2;BP1;SP5,6',
                                'BP1,2;BP1,2;SP1-3',
                                'BP1,2;BP1,2;SP3-5',
                                'BP1,2;BP1,2;SP4,5',
                                'BP1,2;BP1,2;SP4-6',
                                'BP1,2;BP1,2;SP5-7',
                                'BP1,2;BP1,2;SP6,7',
                                'BP1,2;BP1;BP1,2;SP5-7',
                                'BP1,2;BP1;SP2-4',
                                'BP1,2;BP1;SP3-5',
                                'BP1,2;BP1;SP4-6',
                                'BP1,2;BP2;BP1,2;SP5-7',
                                'BP1,2;BP2;BP1;SP4-6',
                                'BP1,2;BP2;BP1;SP5-7',
                                'BP1,2;SP1-3',
                                'BP1,2;SP2,3',
                                'BP1,2;SP2-4',
                                'BP1,2;SP4-6',
                                'BP1,2;SP5,6',
                                'BP1,2;SP5-7',
                                'BP1,2;SP6,7',
                                'BP1,2;SP6-8',
                                'BP1,2;SP7,8',
                                'BP2;BP1;SP2-4',
                                'BP2;BP1;SP3,4',
                                'BP2;BP1;SP3-5',
                                'C:1H',
                                'C:AC',
                                'C:BC',
                                'C:HEA;HEP',
                                'C:HEP',
                                'C:KN',
                                'C:R01-32',
                                'C:R09-32;PH1-8',
                                'FL',
                                'FS',
                                'FS;SP1',
                                'FS;SP1,2',
                                'FS;SP1-3',
                                'FS;SP2,3',
                                'FS;SP2-4',
                                'FS;SP3,4',
                                'FS;SP3-5',
                                'FS;SP4',
                                'FS;SP4,5',
                                'FS;SP5,6',
                                'HC1,3-7',
                                'HC1-4',
                                'HC1-6',
                                'HC1-6;NC1,2',
                                'HC1-7',
                                'HC1-7;NC1',
                                'HC1-7;NC1,2',
                                'HC1-7;NC2',
                                'HC2,4,6,7',
                                'HC2,4,6,7;NC2',
                                'HC2-7;NC1,2',
                                'HC3-6',
                                'HC3-7',
                                'HC3-7;NC1',
                                'HC3-7;NC1,2',
                                'HC5-7',
                                'HC5-7;NC1',
                                'HC7;NC1,2',
                                'HC7;NC1,2;SP2-5',
                                'HE1-4',
                                'HE1-4;NE1,2',
                                'HE1-4;NE2',
                                'HEA;HEP',
                                'HEA;HEP;NEA;NEP',
                                'HEP',
                                'HHA;HHP',
                                'L11',
                                'NEA;NEP;SP1',
                                'NEP;SP1',
                                'SHL',
                                'SHS',
                                'SP2-4',
                                'SP2-5',
                                'SP3,4',
                                'SP3-5',
                                'SP3-6',
                                'SP4-6',
                                'SP5-7',
                                'T:HEA;HEP',
                                'T:HEP']
    for coil in possible_coil_names:
        rcae = ReceiveCoilActiveElements(coil)
        print(str(rcae))
        print(rcae.get_value())

