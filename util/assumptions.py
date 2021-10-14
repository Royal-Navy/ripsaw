""" This is a file of functions and objects that might be refactored out entirely or make short-term coupling."""


def chromo_dict_generator(cwd, cmd_args,
                          input_filename, chromosome, region_identifier,
                          output_score_func, output_filename,
                          get_log_func, log_filename,
                          optimiser_dict):
    """ Generate dictionaries based on supplied parameters.

    This is more convenient for now while the functional parametrisation is worked on."""

    genotype_dict = {  # Create mock genotype dictionary
        'files': [
            {
                'URL': input_filename,
                'region_value':
                    {
                        region_identifier: chromosome,
                    },
            }
        ]
    }

    output_dict = {
        'files': [
            {
                'URL': output_filename,
                'function': output_score_func
            }
        ]
    }

    execute_dict = {
        'files': [
            {
                'suppress_output': True,
                'URL': cmd_args,
                'cwd': cwd,
                'as_admin': False
            }
        ]
    }

    log_dict = {
        'files': [
            {
                'URL': log_filename,
                'function': get_log_func,
                'as_admin': False
            }
        ]
    }

    return genotype_dict, output_dict, execute_dict, log_dict
