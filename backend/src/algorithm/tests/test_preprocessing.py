import unittest
import os
import preprocessing

class TestPreprocessing(unittest.TestCase):

    def test_image_validated(self):
        invalid_file_name = "corrupted_image.jpg"
        valid_file_name = "valid_image.jpg"
        invalid_path = "/invalid/path"
        valid_path = os.getcwd()
        with self.assertRaises(FileExistsError):
            preprocessing.produce_depth_map(invalid_path, invalid_file_name)
        with self.assertRaises(FileNotFoundError):
            preprocessing.produce_depth_map(valid_path, invalid_file_name)
        with self.assertRaises(FileExistsError):
            preprocessing.produce_depth_map(invalid_path, valid_file_name)        

        preprocessing.produce_depth_map(valid_path, valid_file_name)
        self.assertTrue()



if __name__ == '__main__':
    unittest.main()
