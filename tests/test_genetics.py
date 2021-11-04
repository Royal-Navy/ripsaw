"""
Test functionality of genetics objects such as Nuclei, Chromosomes and Genes.

The 'setUp' function creates variables and functions to be used in the unit tests.
"""
import unittest
from unittest.mock import patch
import numpy as np
from ripsaw.genetics.genotype import AbstractGene, Chromosome
from ripsaw.genetics.crossovers import point_crossover, multiple_crossovers
from ripsaw.genetics.selection import roulette, uniform_random
from ripsaw.genetics.optimiser import Optimiser
import os
import sys
from tests.test_env_wrapper import TestEnvWrapper

# logging.getLogger().setLevel(logging.DEBUG)


class TestProgramXGene(AbstractGene):
    def __init__(self, chromosome=None):
        self.value = None
        self.chromosome = chromosome
        self.create()

    def __str__(self):
        return "X\n" + str(self.value) + "\n"
        pass

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def create(self):
        self.value = np.random.uniform(-5, 5)

    def mutate(self):
        self.value = np.random.uniform(-5, 5)

        if self.chromosome:
            self.chromosome.reset_fitness()


class TestProgramZGene(AbstractGene):
    def __init__(self, chromosome=None):
        self.value = None
        self.chromosome = chromosome
        self.create()

    def __str__(self):
        return "Y\n" + str(self.value) + "\n"
        pass

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def create(self):
        self.value = np.random.uniform(-5, 5)

    def mutate(self):
        clipped_val = np.random.uniform(-5, 5)

        self.value = clipped_val

        if self.chromosome:
            self.chromosome.reset_fitness()


class TestGene(AbstractGene):
    pass


class TestGenetics(unittest.TestCase):
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
            raise Exception("Result couldn't be found - was the file created? URL:" + str(output_file))

    @staticmethod
    def multi_gene_chromosome_function(chromosome, num_chromo=3):
        genes = []
        for i in range(num_chromo):
            genes.append(TestProgramXGene(chromosome=chromosome))

        return genes

    @staticmethod
    def for_test_program_chromosome_function(chromosome):
        return [TestProgramXGene(chromosome=chromosome),
                TestProgramZGene(chromosome=chromosome)]

    @staticmethod
    def test_log_dummy_function():
        return list()

    @staticmethod
    def example_entropy_function(optimiser_dict):
        return optimiser_dict['epoch_num'] * 2

    @staticmethod
    def index_distribution_function(i):
        """
        Given an index of a gene, return the probability that this is a crossover point.
        For the purposes of testing, this is hardcoded to 1.0 if 1.
        :param i: The integer index
        :return: The float probability of selection.
        """
        if i == 1:
            return 1.0
        else:
            return 0.0

    @staticmethod
    def get_output_log(filepath):
        output_row = list()

        with open(filepath, 'r') as in_fs:
            for i, line in enumerate(in_fs.readlines()):
                output_row.append(line)

        return output_row

    def test_chromo_mutate_fitness_reset(self):
        chromosome = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome.fitness = 1
        chromosome.mutate(p_total_mutate=1.0)
        self.assertNotEqual(1, chromosome.fitness)

    def test_chromo_total_mutate(self):
        chromosome = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome.fitness = 1
        chromosome.mutate(p_total_mutate=1.0)
        self.assertNotEqual(1, chromosome.fitness)

    def test_type_interpretation(self):
        chromosome = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)

        chromosome.fitness = 1.0
        self.assertEqual(1, int(chromosome))

        chromosome.fitness = 1
        self.assertEqual(1.0, float(chromosome))

    def test_abstract_gene(self):
        catching_error = False
        try:
            TestGene()
        except TypeError as e:
            catching_error = True

        self.assertTrue(catching_error)

    @patch.multiple(AbstractGene, __abstractmethods__=set())
    def test_abstract_methods(self):
        instance = AbstractGene()
        instance.mutate()
        instance.create()
        instance.__str__()

    def test_gene_creation(self):
        gene = TestProgramXGene()

        self.assertEqual(str, type(str(gene)))

    def test_chromosome_creation(self):
        chromosome = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        self.assertEqual(None, chromosome.fitness)
        self.assertEqual(TestGenetics.multi_gene_chromosome_function, chromosome.chromosome_function)
        self.assertEqual(3, len(chromosome.full_genotype))

    def test_chromosome_execute(self):
        chromosome = Chromosome(chromosome_function=TestGenetics.for_test_program_chromosome_function)
        cwd = "sample_program_template"
        if os.name == "nt":
            exe_file_path = os.path.join('sample_program_template', 'run_program.bat')
        else:
            exe_file_path = os.path.join('sample_program_template', 'run_program.sh')
        target_dir_path = os.path.dirname(os.path.abspath(__file__))
        input_file_path = os.path.join('sample_program_template', 'input.txt')
        region_identifier = '<region1>\n'
        output_score_func = TestEnvWrapper.get_output_score_func
        output_file_path = os.path.join('sample_program_template', 'output.txt')
        output_log_func = TestGenetics.get_output_log
        output_log_path = os.path.join('sample_program_template', 'output.txt')

        chromosome.setup(cwd, exe_file_path, target_dir_path,
                         input_file_path, region_identifier,
                         output_score_func, output_file_path,
                         output_log_func, output_log_path,
                         optimiser_dict={"epoch_num": 0})
        chromosome.evaluate()

        print("Fitness", chromosome.fitness)

    def example_conf_function(self):
        pass

    def test_optimiser(self):
        cwd = "sample_program_template"
        if os.name == "nt":
            exe_file_path = os.path.join('sample_program_template', 'run_program.bat')
        else:
            exe_file_path = os.path.join('sample_program_template', 'run_program.sh')
        target_dir_path = os.path.dirname(os.path.abspath(__file__))
        input_file_path = os.path.join('sample_program_template', 'input.txt')
        region_identifier = '<region1>\n'
        output_score_func = TestEnvWrapper.get_output_score_func
        output_file_path = os.path.join('sample_program_template', 'output.txt')
        population_size = 10
        chromosome_function = TestGenetics.for_test_program_chromosome_function
        num_xovers = 4
        num_xover_points = 1
        p_gene_mutate = 1 / 2
        p_total_mutate = 1 / 2
        output_log_func = TestGenetics.get_output_log
        output_log_path = os.path.join('sample_program_template', 'output.txt')

        optimiser = Optimiser(population_size=population_size, chromosome_function=chromosome_function,
                              num_xovers=num_xovers, num_xover_points=num_xover_points,
                              p_gene_mutate=p_gene_mutate, p_total_mutate=p_total_mutate,
                              cwd=cwd, parallel_exe=False, exe_file_path=exe_file_path, target_dir_path=target_dir_path,
                              input_file_path=input_file_path, region_identifier=region_identifier,
                              output_score_func=output_score_func, output_file_path=output_log_path,
                              output_log_func=output_log_func, output_log_file=output_log_path,
                              target_score=1.9)

        optimiser.run()

    def test_point_crossover(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)

        chromosomes = [chromosome0, chromosome1]

        identical = True
        for i in range(100):
            offspring = point_crossover(chromosomes=chromosomes, num_points=1)

            self.assertEqual(2, len(offspring))
            self.assertEqual(3, len(offspring[0].full_genotype))
            self.assertEqual(3, len(offspring[1].full_genotype))

            for j in range(len(chromosomes)):
                for gene_a in chromosomes[j].full_genotype:
                    for gene_b in offspring[j]:
                        if gene_a != gene_b:
                            identical = False

        self.assertEqual(False, identical)

    def test_two_point_crossover(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)

        chromosomes = [chromosome0, chromosome1]

        identical = True
        for i in range(100):
            offspring = point_crossover(chromosomes=chromosomes, num_points=2)

            self.assertEqual(2, len(offspring))
            self.assertEqual(3, len(offspring[0].full_genotype))
            self.assertEqual(3, len(offspring[1].full_genotype))

            for j in range(len(chromosomes)):
                for gene_a in chromosomes[j].full_genotype:
                    for gene_b in offspring[j]:
                        if gene_a != gene_b:
                            identical = False

        self.assertEqual(False, identical)

    def test_two_point_crossover_distribution(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)

        chromosomes = [chromosome0, chromosome1]

        identical = True
        for i in range(50):
            offspring = point_crossover(chromosomes=chromosomes, num_points=2,
                                        index_distribution=TestGenetics.index_distribution_function)

            self.assertEqual(2, len(offspring))
            self.assertEqual(3, len(offspring[0].full_genotype))
            self.assertEqual(3, len(offspring[1].full_genotype))

            for j in range(len(chromosomes)):
                for k in range(len(chromosomes[j])):
                    if chromosomes[j][k] is not offspring[j][k]:
                        identical = False

        self.assertEqual(False, identical)

    def test_multiple_crossover_distribution(self):
        identical = True
        for i in range(100):
            chromosomes = list()

            for _ in range(10):
                chromosomes.append(Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function))

            offspring = multiple_crossovers(parent_chromosomes=chromosomes, num_points=1, chrom_per_crossover=2,
                                            index_distribution=TestGenetics.index_distribution_function)

            self.assertEqual(10, len(offspring))
            for _offspring in offspring:
                self.assertEqual(3, len(_offspring))

            for j in range(len(chromosomes)):
                for k in range(len(chromosomes[j])):
                    if chromosomes[j][k] is not offspring[j][k]:
                        identical = False
        self.assertEqual(False, identical)

    def test_multiple_crossover_one_remaining(self):
        identical = True
        for i in range(50):
            chromosomes = list()

            for _ in range(10):
                chromosomes.append(Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function))

            offspring = multiple_crossovers(parent_chromosomes=chromosomes, num_points=1, chrom_per_crossover=3)

            self.assertEqual(10, len(offspring))
            for _offspring in offspring:
                self.assertEqual(3, len(_offspring))

            for j in range(len(chromosomes)):
                for k in range(len(chromosomes[j])):
                    if chromosomes[j][k] is not offspring[j][k]:
                        identical = False
        self.assertEqual(False, identical)

    def test_multiple_crossover_three_remaining(self):
        identical = True
        # ToDO Review deep copy and 'identical' checking in multi-crossover function which uses a deepcopy.
        for i in range(50):
            chromosomes = list()

            for _ in range(15):
                chromosomes.append(Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function))

            offspring = multiple_crossovers(parent_chromosomes=chromosomes, num_points=2, chrom_per_crossover=4)

            self.assertEqual(15, len(offspring))
            for _offspring in offspring:
                self.assertEqual(3, len(_offspring))

            for j in range(len(chromosomes)):
                for k in range(len(chromosomes[j])):
                    if chromosomes[j][k] is not offspring[j][k]:
                        identical = False
        self.assertEqual(False, identical)

    def test_roulette_selection(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome0.fitness = 2
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1.fitness = 1
        chromosomes = [chromosome0, chromosome1]

        counter = 0
        for i in range(1000):
            selection = roulette(chromosomes, num_samples=1, duplicates=False)

            if selection[0].fitness == 2:
                counter += 1

        in_range = (500 < counter < 666 + 66)
        # Intuitively you might expect a result of 666 on average, but roulette
        # compensates for negative values by adding the smallest value to the rest.
        # this skews selection probability slightly toward lower values if lowest fitness is +ve.

        print("Roulette Counter:", counter)
        self.assertTrue(in_range)

    def test_roulette_selection_zero_fitness_case_self(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome0.fitness = 0
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1.fitness = 0
        chromosomes = [chromosome0, chromosome1]

        counter = 0
        for i in range(1000):
            selection = roulette(chromosomes, num_samples=1, duplicates=False)

            if selection[0] is chromosome0:
                counter += 1

        in_range = (440 < counter < 560)

        print("Roulette Counter Zero Case:", counter)
        self.assertTrue(in_range)

    def test_uniform_selection(self):
        chromosome0 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome0.fitness = 2
        chromosome1 = Chromosome(chromosome_function=TestGenetics.multi_gene_chromosome_function)
        chromosome1.fitness = 1
        chromosomes = [chromosome0, chromosome1]

        counter = 0
        for i in range(1000):
            selection = uniform_random(chromosomes, num_samples=1, duplicates=False)

            if selection[0].fitness == 2:
                counter += 1

        in_range = (450 < counter < 550)

        print("Uniform Counter:", counter)
        self.assertTrue(in_range)

    def setUp(self):
        self.genotype_dict = {  # Create mock genotype dictionary
            'files': [
                {
                    'URL': 'test.inp',
                    'region_value':
                        {
                            'x': 'test_output1\n',
                            'z': 'test_output2\n'
                        }
                }
            ]
        }

        self.execute_dict = {
            'files': [
                {
                    'suppress_output': False,
                    'URL': [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         'sample_program', 'optimisation_program.py')],
                    'cwd': os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'sample_program')
                }
            ]
        }

        self.output_dict = {
            'files': [
                {
                    'URL': os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'sample_program', 'output.txt'),
                    'function': self.get_output_score_func
                }
            ]
        }

        with open("test.inp", 'w') as in_fs:
            input_file_contents = """
            x
            <region1>
            y
            <region2>
            """
            in_fs.writelines(input_file_contents)


if __name__ == '__main__':
    unittest.main()
