from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock
from app.EventManager import PatternVariant , FrequencyManager


class test_frequency_pattern(unittest.TestCase):
    def setUp(self) -> None:
        # set up
        self.FM = FrequencyManager(PatternVariant())
        self.PV  = PatternVariant()
        self.result = None
    def tearDown(self) -> None:
        # clean up
        pass
    def processingData(self,data):
        unzipped_object = zip(*data['data'])
        unzipped_list = list(unzipped_object)  
        self.FM.addIncomingData(unzipped_list)
        self.result = self.FM.PatternProcessor(data['address'])


    def test_fastFlash_valid(self):
        data = {
            'data': [(1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1)], 
            'address': ('port1', 'port2', 'port3')
            }
        
        self.processingData(data)
        PV = self.PV

        result = self.result
        
        self.assertEqual(result['port1']['type'],PV.FastFlashing.__name__)
        self.assertEqual(result['port2']['type'],PV.SolidOff.__name__)
        self.assertEqual(result['port3']['type'],PV.SolidOn.__name__)

    def test_fastFlash_invalid(self):
        data = {
            'data': [(1, 2, 1), (1, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1), (1, 2, 1), (2, 2, 1)], 
            'address': ('port1', 'port2', 'port3')
            }
        self.processingData(data)
        PV = self.PV

        result = self.result

        print(result)
        self.assertNotEqual(result['port1']['type'],PV.FastFlashing.__name__)
        self.assertEqual(result['port2']['type'],PV.SolidOff.__name__)
        self.assertEqual(result['port3']['type'],PV.SolidOn.__name__)


    def test_solidOnsolidOff_valid(self):
        data = {
            'data': [(1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1), (1, 2, 1)],
            'address': ('port1', 'port2', 'port3')
            }
        self.processingData(data)
        PV = self.PV

        result = self.result
        
        self.assertEqual(result['port1']['type'],PV.SolidOn.__name__)
        self.assertEqual(result['port2']['type'],PV.SolidOff.__name__)
        self.assertEqual(result['port3']['type'],PV.SolidOn.__name__)

    def test_solidOnsolidOff_4tower_valid(self):
        data = {
            'data': [(1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1,1), (1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1, 1), (1, 2, 1, 1)],
            'address': ('port1', 'port2', 'port3','port4')
            }
        self.processingData(data)
        PV = self.PV

        result = self.result
        
        self.assertEqual(result['port1']['type'],PV.SolidOn.__name__)
        self.assertEqual(result['port2']['type'],PV.SolidOff.__name__)
        self.assertEqual(result['port3']['type'],PV.SolidOn.__name__)
        self.assertEqual(result['port4']['type'],PV.SolidOn.__name__)

