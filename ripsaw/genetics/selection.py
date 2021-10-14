import numpy.random as npr
import numpy as np
import sys
import logging


def roulette(population, num_samples, duplicates=False):
    """
    Select a determined number of samples from the population, p(select) weighted by population fitness.
    :param population:
    A list of chromosomes.
    :param num_samples:
    The number of chromosomes to select
    :param duplicates:
    If duplicate chromosomes are permitted.
    :return population:
    List of selected chromosomes.
    """
    min_fitness = min([chromosome.fitness for chromosome in population])
    logging.debug("min fitness: " + str(min_fitness))
    fitnesses = list()
    for chromosome in population:
        fitnesses.append(chromosome.fitness + abs(min_fitness) + sys.float_info.epsilon)
    total_fitness = sum(fitnesses)

    if total_fitness == 0:  # Avoid divide by zero
        return uniform_random(population, num_samples, duplicates)

    selection_prob = np.asarray([fitness / total_fitness for fitness in fitnesses])

    logging.debug("Selection probability: " + str(selection_prob))
    selected_indices = npr.choice(a=len(population), p=selection_prob, size=num_samples, replace=duplicates)
    logging.debug("Selected parent indices:" + str(selected_indices))
    returned_chromos = list()
    for i in selected_indices:
        returned_chromos.append(population[i])

    return returned_chromos


def uniform_random(population, num_samples, duplicates=False):
    """
    Select a determined number of chromosomes from the population at random.
    :param population:
    A list of chromosomes.
    :param num_samples:
    The number of chromosomes to select
    :param duplicates:
    If duplicate chromosomes are permitted.
    :return:
    List of selected chromosomes.
    """

    selected_indices = npr.choice(a=len(population), size=num_samples, replace=duplicates)

    returned_chromos = list()
    for i in selected_indices:
        returned_chromos.append(population[i])

    return returned_chromos
