from django.test import TestCase

# Create your tests here.
import unittest
import math
from core.views import haversine
 # اختبار اخذ موقع العميل واعطاء المسافة الاقرب اليه

class TestHaversine(unittest.TestCase):
    def test_distance(self):
        # إحداثيات القاهرة والرياض
        lat1, lon1 = 30.0444, 31.2357  # القاهرة
        lat2, lon2 = 24.7136, 46.6753  # الرياض

        # القيمة المتوقعة للمسافة بين القاهرة والرياض (تقريبًا 1636 كم)
        expected_distance = 1636  
        
        # حساب المسافة باستخدام الدالة
        calculated_distance = haversine(lat1, lon1, lat2, lon2)
        
        # اختبار أن المسافة المحسوبة قريبة من المتوقع بفارق لا يزيد عن ±5 كم
        self.assertAlmostEqual(calculated_distance, expected_distance, delta=5)
 