import time


class Logger:
    def __init__(self, target_file=None, user_headers=list(), num_chromosomes=None, num_user_output=None):

        if target_file:
            self.target_file = target_file
        else:
            start_time = time.time()
            self.target_file = "output_" + str(start_time)[1:-8] + ".csv"

        default_header = ['epoch', 'creation_epoch', 'uuid', 'fitness']
        default_header.extend(user_headers)
        self.log_to_csv(default_header)

    def log_to_csv(self, log_row):
        """ This function logs a list into a csv format."""
        with open(self.target_file, 'a') as out_fs:
            for value in log_row:
                out_fs.write(str(value) + ",")
            out_fs.write("\n")
