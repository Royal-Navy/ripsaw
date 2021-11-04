"""
Definitions for Chromosomes and Genes.

"""

from abc import ABC, abstractmethod
import numpy as np
from ripsaw.util.assumptions import chromo_dict_generator
from ripsaw.local_env_wrapper import LocalEnvWrapper
import hashlib
import logging


class Chromosome:
    def __init__(self, chromosome_function,
                 passed_genes=None):
        """
        A chromosome object contains a list of genes.
        It can mutate or be turned into a phenotype by using it's __overrides__.
        :param chromosome_function:
        A function which takes mutation probabilities to return a list of genes.
        :param passed_genes:
        A list of genes to set as the genotype of this chromosome, rather than use the genotype function as default.
        """
        self.fitness = None
        self.uuid = None
        self.user_output_log = None
        self.epoch_number = None
        self.creation_epoch_number = None

        self.log_row = None

        self.genotype_dict = None
        self.output_dict = None
        self.execute_dict = None
        self.log_dict = None
        self.target_dir = None
        self.chromosome_function = chromosome_function

        if passed_genes:
            self.full_genotype = passed_genes
        else:
            self.generate_genotype()

        self.reset_fitness()

    def generate_genotype(self):
        """ Run the chromosome function and establish the full genotype as a list of Gene objects."""
        self.full_genotype = self.chromosome_function(chromosome=self)

    def setup(self, cwd, cmd_args, target_dir,
              input_file_path, region_identifier,
              output_score_func, output_filename,
              output_log_func, output_log_file,
              optimiser_dict):

        """ Prepare this chromosome for evaluation."""

        if self.fitness is None:
            self.creation_epoch_number = optimiser_dict["epoch_num"]

            dicts = chromo_dict_generator(cwd, cmd_args, input_file_path,
                                          self, region_identifier,
                                          output_score_func, output_filename,
                                          output_log_func, output_log_file,
                                          optimiser_dict)

            self.target_dir = target_dir
            (self.genotype_dict, self.output_dict, self.execute_dict, self.log_dict) = dicts

    def evaluate(self):
        """ Run the target program, setting this chromosomes fitness and getting logs from the target folder."""
        if self.fitness is None:
            wrapper = LocalEnvWrapper(folder=self.target_dir)
            wrapper.set_input_files(genotype_setup=self.genotype_dict)
            wrapper.execute(execution_dict=self.execute_dict)

            self.fitness = wrapper.get_output_score(get_output_dict=self.output_dict)

            self.user_output_log = wrapper.get_log_row(log_dict=self.log_dict)
            self.set_log_row()

    def set_log_row(self):
        """ Return a row for the csv logger. First take info about this chromo and then append user supplied function"""
        self.log_row = list()

        self.log_row.append(self.creation_epoch_number)
        self.log_row.append(self.uuid)
        self.log_row.append(self.fitness)

        for gene in self.full_genotype:
            self.log_row.append(str(gene).replace("\n", " "))
            self.log_row.append(int(gene))
            self.log_row.append(float(gene))

        self.log_row.extend(self.user_output_log)

    def get_log_row(self):
        """ Pass up the logging from this object and the user supplied one which ran on the target environment."""
        return self.log_row

    def mutate(self, p_gene_mutate=0, p_total_mutate=0, **mutate_params):
        """
        Call the Chromosome's genotype function, using it's mutation probabilities.
        Additionally, the mutate_params will be supplied to the genotype function. This could include the information
        about the optimiser's state i.e the generation number, standard deviation etc.
        :param p_gene_mutate:
        Probability that a single gene is mutated.
        :param p_total_mutate:
        Probability that an entire chromosome is mutated.
        :param mutate_params:
        One or many parameters i.e probabilities=[0.1, 0.9], gen_number=1, std_dev=1 etc.
        :return: None
        """

        if np.random.random() <= p_total_mutate:
            logging.debug("Total Mutating: " + str(self.uuid) + " Fitness: " + str(self.fitness))
            self.generate_genotype()
            self.reset_fitness()

        for gene in self.full_genotype:
            if np.random.random() <= p_gene_mutate:
                logging.debug("Gene Mutating: " + str(self.uuid) + " Fitness: " + str(self.fitness))
                gene.mutate(**mutate_params)
                self.reset_fitness()

    def reset_fitness(self):
        """ Set the fitness back to it's default value."""
        self.set_unique_id()
        self.fitness = None

    def get_fitness(self):
        """ Get the 'value' of this chromosome. """
        return self.fitness

    def set_unique_id(self):
        """ Use a hashing feature on the string value to determine a unique ID."""
        hash_object = hashlib.sha256(str(self).encode())
        hex_dig = hash_object.hexdigest()
        self.uuid = hex_dig

    def __len__(self):
        """ Get the length value of this chromosome object."""
        return len(self.full_genotype)

    def __float__(self):
        """Get the floating point value of this chromosome object."""
        return float(self.fitness)

    def __int__(self):
        """ Get the integer value approximation of this chromosome object."""
        return int(self.fitness)

    def __str__(self):
        """ Get the string value of the genotype of this object."""
        value = ""
        for gene in self.full_genotype:
            value += str(gene)
        return value

    def __getitem__(self, key):
        return self.full_genotype[key]


class AbstractGene(ABC):
    """ This is the base class for Genes. It can be used to create Genes that have a requirement of implementation."""
    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
