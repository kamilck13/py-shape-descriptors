from unittest import TestCase


from descriptors.circularity.circularity import circularity
from descriptors.datasets.common import _load_dataset


class TestCircularity(TestCase):
    def test_C_h(self):
        images = _load_dataset(file_path='C:\pyshape\\', dataset_name='regular_polygons', ext="*.png")

        vals = {
            'r03': 0.8270,
            'r04': 0.9549,
            'r05': 0.9833,
            'r06': 0.9924,
            'r07': 0.9960,
            'r08': 0.9977,
            'r09': 0.9986,
            'r10': 0.9991,
            'r11': 0.9994,
            'r12': 0.9996
        }
        for k, v in images.items():
            print("{0} {1:.4f} {2:.4f}".format(k, circularity(v), vals[k[:-4]]))
            self.assertAlmostEqual(circularity(v), vals[k[:-4]], 4)


    def test_Cst(self):
        images = _load_dataset(file_path='C:\pyshape\\', dataset_name='regular_polygons', ext="*.png")

        vals = {
            'r03': 0.6097,
            'r04': 0.7937,
            'r05': 0.8682,
            'r06': 0.9128,
            'r07': 0.9349,
            'r08': 0.9532,
            'r09': 0.9622,
            'r10': 0.9712,
            'r11': 0.9653,
            'r12': 0.9811
        }
        for k, v in images.items():
            print("{0} {1:.4f} {2:.4f}".format(k, circularity(v, 'Cst'), vals[k[:-4]]))
            self.assertAlmostEqual(circularity(v, 'Cst'), vals[k[:-4]], 4)