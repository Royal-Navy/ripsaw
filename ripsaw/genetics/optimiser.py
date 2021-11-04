from ripsaw.genetics.selection import roulette
from ripsaw.genetics.crossovers import point_crossover
from ripsaw.genetics.genotype import Chromosome
from ripsaw.util.logging import Logger

import math
import time
import logging
import multiprocessing as mp
from datetime import datetime


class Optimiser:
    def __init__(self, population_size, chromosome_function,
                 num_xovers, num_xover_points,
                 p_gene_mutate, p_total_mutate,
                 cwd, parallel_exe, exe_file_path, target_dir_path,
                 input_file_path, region_identifier,
                 output_score_func, output_file_path,
                 output_log_func, output_log_file,
                 target_score=math.inf, num_epochs=math.inf, max_time=math.inf,
                 population=list()):

        # Object parameterisation
        self.population_size = population_size
        self.chromosome_function = chromosome_function
        self.num_xovers = num_xovers
        self.num_xover_points = num_xover_points
        self.p_gene_mutate = p_gene_mutate
        self.p_total_mutate = p_total_mutate
        self.cwd = cwd
        self.exe_file_path = exe_file_path
        self.parallel_exe = parallel_exe
        self.target_dir_path = target_dir_path
        self.input_file_path = input_file_path
        self.region_identifier = region_identifier
        self.output_score_func = output_score_func
        self.output_file_path = output_file_path
        self.output_log_func = output_log_func
        self.output_log_file = output_log_file
        self.target_score = target_score
        self.num_epochs = num_epochs
        self.max_time = max_time
        self.population = population

        # Internal Fields
        self.epoch_number = None
        self.logger = None
        self.best_score = None
        self.mean_score = None
        self.std_dev_score = None
        self.internal_dict = {"epoch_num": 0}

    @staticmethod
    def evaluate(chromosome):
        """ For the purposes of multiprocessing, this is a mapped function for a list of chromosomes."""
        chromosome.evaluate()

        return chromosome

    @staticmethod
    def sort_chromosome_key(chromosome):
        """ Designed to put None before lowest fitness. None at the end was interfering with immortal logic on sort."""
        fitness = chromosome.get_fitness()

        if fitness is None:
            return -math.inf
        else:
            return fitness

    @staticmethod
    def stopping_criteria_met(start_time, max_time, current_epoch, max_epochs, best_score, target_score):
        """ We go through some stopping criteria. If any are met, True is returned."""

        if best_score >= target_score:
            return True
        if time.time() - start_time > max_time:
            return True
        if current_epoch >= max_epochs:
            return True

        return False

    def epoch(self, chromosomes=list()):
        """ Going through the Evaluate -> Selection -> Crossover -> Mutation process once as an epoch."""

        logging.debug("At start of epoch - Chromo fitness in order:" +
                      str([chromosome.fitness for chromosome in chromosomes]))

        # 1. Generate new chromosomes for each missing
        to_generate = self.population_size - len(chromosomes)

        for _ in range(to_generate):
            chromosomes.append(Chromosome(chromosome_function=self.chromosome_function))

        # 2. Evaluate every chromosome which doesn't have a fitness.
        for chromosome in chromosomes:
            chromosome.setup(self.cwd, self.exe_file_path, self.target_dir_path,
                             self.input_file_path, self.region_identifier,
                             self.output_score_func, self.output_file_path,
                             self.output_log_func, self.output_log_file,
                             self.internal_dict
                             )

        if self.parallel_exe:
            with mp.Pool(int(mp.cpu_count())-2) as p:
                chromosomes = p.map(Optimiser.evaluate, chromosomes)
        else:
            for chromosome in chromosomes:
                chromosome.evaluate()

        # 3. Logging
        for chromosome in chromosomes:
            optimiser_log = [self.internal_dict["epoch_num"]]
            optimiser_log.extend(chromosome.get_log_row())
            self.logger.log_to_csv(optimiser_log)

        chromosomes.sort(key=Optimiser.sort_chromosome_key)
        logging.debug("Before Crossover - Chromo fitness in order:" +
                      str([chromosome.fitness for chromosome in chromosomes]))

        scores = [chromosome.get_fitness() for chromosome in chromosomes]
        self.best_score = max(scores)
        self.mean_score = sum([chromosome.get_fitness() for chromosome in chromosomes]) / self.population_size
        self.std_dev_score = sum([abs(self.mean_score - score) for score in scores]) / self.population_size

        # 4. Crossovers
        selection = roulette(population=chromosomes, num_samples=self.num_xovers)

        offspring = point_crossover(chromosomes=selection, num_points=self.num_xover_points)

        chromosomes = chromosomes[len(offspring):]  # Cull the weakest.
        chromosomes.extend(offspring)

        # 5. Mutate
        chromosomes.sort(key=Optimiser.sort_chromosome_key)
        logging.debug("After Crossover - Chromo fitness in order:" +
                      str([chromosome.fitness for chromosome in chromosomes]))

        for i, chromosome in enumerate(chromosomes):
            if chromosome.fitness != self.best_score:  # The minus one offset is to protect the immortal.
                chromosome.mutate(p_gene_mutate=self.p_gene_mutate,
                                  p_total_mutate=self.p_total_mutate)
            else:
                logging.debug("Immortal protected, fitness:" + str(chromosomes[i].get_fitness()))

        return chromosomes

    def run(self):
        """ In Charge of running epochs until a stopping criteria is met."""

        self.best_score = -math.inf
        start_time_s = time.time()
        start_time_dt = datetime.now()

        start_time_hhmmss = start_time_dt.strftime("%H:%M:%S")
        self.logger = Logger()

        print("Starting the optimiser...")
        print("\tStart Time: ", start_time_hhmmss)
        while Optimiser.stopping_criteria_met(start_time=start_time_s, max_time=self.max_time,
                                              current_epoch=self.internal_dict["epoch_num"], max_epochs=self.num_epochs,
                                              best_score=self.best_score, target_score=self.target_score) is not True:

            self.population = self.epoch(chromosomes=self.population)
            self.internal_dict["epoch_num"] += 1
            current_time_dt = datetime.now()

            print("Epoch", str(self.internal_dict["epoch_num"]), "done.")
            print("\tBest score: ", self.best_score)
            print("\tAverage Score: ", self.mean_score)
            print("\tStandard Deviation: ", self.std_dev_score)
            print("\tTime elapsed: ", current_time_dt - start_time_dt)
