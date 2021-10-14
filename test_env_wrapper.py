"""
Test functionality of the local environment wrapper.

The 'setUp' function creates variables and functions to be used in the unit tests.
"""
import unittest
import os
from ripsaw import local_env_wrapper


class TestEnvWrapper(unittest.TestCase):
    @staticmethod
    def get_output_score_func(output_file):
        """
        A tests function for stripping output scores from a tests file.
        :param output_file:
        :return:
        """
        with open(output_file, 'r') as in_fs:
            for line in in_fs.readlines():
                if "Result" in line:
                    tokens = line.split(" ")
                    return tokens[-1]
            raise Exception("Result couldn't be found - was the file created?")

    def test_execute(self):
        """
        A can of worms otherwise, so we just check to ensure the method is there and functions.
        """
        self.wrapper.execute(self.execute_dict)

    def test_execute_supressed(self):
        self.execute_dict['files'][0]['suppress_output'] = True

        self.wrapper.execute(self.execute_dict)

    def test_set_input_files(self):
        """
        Set the input files using a tests genotype_dict (see setUp). Tests the values were set as intended.
        """
        self.wrapper.set_input_files(genotype_setup=self.genotype_dict)

        file = os.path.join(self.wrapper.folder, 'test.inp')
        region_1_val = None
        with open(file, 'r') as in_fs:
            lines = in_fs.readlines()

            for i, line in enumerate(lines):
                if 'x' in line:
                    region_1_val = lines[i+1]
                if 'y' in line:
                    region_2_val = lines[i+1]

        self.assertEqual('test_output1', region_1_val[:-1])

    def test_get_output_score(self):
        """
        Get a with a tests output dict and then check it's correct against the setUp file.
        """
        score = self.wrapper.get_output_score(get_output_dict=self.output_dict)
        self.assertEqual(123, score)

    def setUp(self):
        """
        All the components we need for the other unit tests in this file.
        """
        # In file
        with open("test.inp", 'w') as in_fs:
            input_file_contents = """
            x
            <region1>
            y
            <region2>
            """
            in_fs.writelines(input_file_contents)

        # Out file
        with open("test.out", 'w') as out_fs:
            out_file_contents = """
            Result was 123.\n
            """
            out_fs.writelines(out_file_contents)

        # Wrapper
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.wrapper = local_env_wrapper.LocalEnvWrapper(folder=current_folder)

        # Input dicts
        self.genotype_dict = {  # Create mock genotype dictionary
                        'files': [
                                    {
                                        'URL': 'test.inp',
                                        'region_value':
                                            {
                                                '<region1>': 'test_output1\n',
                                            }
                                    }
                                  ]
                        }

        self.output_dict = {
            'files': [
                        {
                            'URL': 'test.out',
                            'function': self.get_output_score_func
                        }
                    ]
                }

        if os.name == "nt":
            print("Detected Windows")
            self.execute_dict = {
                'files': [
                    {
                        'suppress_output': False,
                        'URL': os.path.join('sample_program_template', 'run_program.bat'),
                        'cwd': 'sample_program_template',
                        'as_admin': False
                    }
                ]
            }
        else:
            print("Detected Linux")
            self.execute_dict = {
                'files': [
                    {
                        'suppress_output': False,
                        'URL': os.path.join('sample_program_template', 'run_program.sh'),
                        'cwd': 'sample_program_template',
                        'as_admin': True
                    }
                ]
            }

    def tearDown(self):
        os.remove("test.inp")
        os.remove("test.out")


if __name__ == '__main__':
    unittest.main()
