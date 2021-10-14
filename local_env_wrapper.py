"""
The local environment wrapper.

Execution is expected to be on a single, multi-core machine with no networking.
"""

import subprocess
import ripsaw.util.file
import os


class LocalEnvWrapper:
    def __init__(self, folder, use_uuid=True, delete_files=True):
        self.use_uuid = use_uuid
        self.delete_files = delete_files

        if use_uuid:
            self.folder = ripsaw.util.file.clone_directory_uuid(source=folder)
        else:
            self.folder = folder

    def set_input_files(self, genotype_setup):
        """
        For every file in the genotype setup, insert genes in defined regions
        :param genotype_setup: A dictionary of the files, regions and corresponding genes.
        """
        for file in genotype_setup['files']:
            url = os.path.join(self.folder, file['URL'])
            region_value = file['region_value']
            self.set_input_file(url=url, region_value=region_value)

    @staticmethod
    def set_input_file(url, region_value):
        """"
        Open up a file by it's URL, then replace region IDs (region) with their values.
        This overwrites the files.
        :param url : file path of an input file.
        :param region_value : a dictionary of 'files'(see unit tests), where value must have a str() value.
        """
        for region, value in region_value.items():
            file_contents = list()

            try:
                with open(url, 'r') as in_fs:
                    for line in in_fs.readlines():
                        if region in line:
                            file_contents.append(str(value) + "\n")
                        else:
                            file_contents.append(line)

                with open(url, 'w') as out_fs:
                    out_fs.writelines(file_contents)
            except FileNotFoundError as e:
                pass
                # import glob
                # print("Error: ", str(e))
                # print("cwd", os.getcwd())
                # for filename in glob.iglob('**/**', recursive=True):
                #     print(filename)

    def get_output_score(self, get_output_dict):
        """
        Open up a series of files and use a function on them.
        :param get_output_dict: a dictionary of 'files'(see unit tests)
        :return: the sum of scores across every function(file).
        """
        score = int()
        for file in get_output_dict['files']:  # file contains 'URL':value for 'function':function
            url = os.path.join(self.folder, file['URL'])
            score += float(file['function'](url))

        return score

    def get_log_row(self, log_dict):
        output_row = list()

        for file in log_dict['files']:  # file contains 'URL':value for 'function':function
            url = os.path.join(self.folder, file['URL'])
            output_row.extend((file['function'](url)))

        return output_row

    def execute(self, execution_dict):
        """
        Open up a series of programs via their executable URL.
        :param execution_dict:  a dictionary of 'files'(see unit tests)
        """
        for file in execution_dict['files']:
            url = os.path.join(self.folder, file['URL'])
            cwd = os.path.join(self.folder, file['cwd'])

            # print("CWD:", os.getcwd())
            # print("Execution cwd:", cwd)
            # print("Execution url:", url)
            cwd = os.path.join(os.getcwd(), cwd)
            url = os.path.join(os.getcwd(), url)
            # print("New cwd: ", cwd)
            # print("Running program with execution URL: ", url,
            #       "\n CWD:", cwd,
            #       "\n Output Supression: ", file['suppress_output'])

            if file['as_admin'] is True:
                execution_payload = ['sudo', url]
            else:
                execution_payload = url

            if file['suppress_output']:
                process = subprocess.Popen(execution_payload, cwd=cwd,
                                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            else:
                process = subprocess.Popen(execution_payload, cwd=cwd)
            process.wait()

            # input("Waiting..")

    def __del__(self):
        if self.use_uuid and self.delete_files:
            ripsaw.util.file.wipe_directory(self.folder)


