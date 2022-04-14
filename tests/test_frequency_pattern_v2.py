from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock
from app.EventManager import  FrequencyManager , PatternVariantInterval


class test_frequency_pattern_v2(unittest.TestCase):
    def setUp(self) -> None:
        # set up
        self.FM = FrequencyManager(PatternVariantInterval())
        self.PV  = PatternVariantInterval()
        self.result = None
    def tearDown(self) -> None:
        # clean up
        pass
    def processingData(self,data):
        unzipped_object = zip(*data['data'])
        unzipped_list = list(unzipped_object)  
        self.FM.addIncomingData(unzipped_list)
        self.result = self.FM.PatternProcessor(data['address'])

    def test_solid_on(self):
     
        self.assertFalse(self.PV.SolidOn(None))
        self.assertFalse(self.PV.SolidOn([1]))
        self.assertFalse(self.PV.SolidOn([]))
        self.assertFalse(self.PV.SolidOn([1, 1, 1, 1, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOn([1, 1, 1, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOn([1, 1, 2, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOn([1, 1, 2, 2, 1, 1, 2, 2]))
        self.assertTrue(self.PV.SolidOn( [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]))
    

    def test_solid_off(self):
     
        self.assertFalse(self.PV.SolidOff(None))
        self.assertFalse(self.PV.SolidOff([1]))
        self.assertFalse(self.PV.SolidOff([]))
        self.assertFalse(self.PV.SolidOff([1, 1, 1, 1, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOff([1, 1, 1, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOff([1, 1, 2, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.SolidOff([1, 1, 2, 2, 1, 1, 2, 2]))
        self.assertFalse(self.PV.SolidOff([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1]))
        self.assertTrue(self.PV.SolidOff([2,2,2,2,2,2,2,2,2,2, 2, 1, 1, 1, 2, 2, 2, 1, 1,2,2,1]))

    
    def test_fast_flash(self):
        self.assertFalse(self.PV.FastFlashing(None))
        self.assertFalse(self.PV.FastFlashing([1]))
        self.assertFalse(self.PV.FastFlashing([]))
        self.assertFalse(self.PV.FastFlashing([1, 1, 1, 1, 1, 2, 2, 2, 2]))
        self.assertFalse(self.PV.FastFlashing([1,1,2,2,2,2,2,1,1]))
        self.assertFalse(self.PV.FastFlashing([1,1,2,2,1,1,2,2,1,1]))
        self.assertFalse(self.PV.FastFlashing([2,2,2,2,2,1,1,1,1]))

        self.assertTrue(self.PV.FastFlashing([1,2,1,2]))
        self.assertTrue(self.PV.FastFlashing([1,2,2,1]))
        self.assertTrue(self.PV.FastFlashing([1,2,2,2,2,2]))
        self.assertTrue(self.PV.FastFlashing([1,2,2,2,2,2,1]))

    
      

