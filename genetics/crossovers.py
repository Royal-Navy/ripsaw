import numpy.random as npr
import numpy as np
from ripsaw.genetics.genotype import Chromosome
import logging
import warnings
import copy


def point_crossover(chromosomes, num_points, index_distribution=None):
    """
    Classic crossover - Select A Single Point and Crossover Either Side.
    :param chromosomes:
    A list of chromosomes objects.
    :param num_points:
    The number of points to crossover.
    :param index_distribution:
    A function which gives a probability of crossover at a given index.
    :return offspring:
    A list of chromosome objects.
    """
    logging.debug("Input Chromosomes: " + str(chromosomes))
    for chromosome in chromosomes:
        logging.debug("Parent:" + str(chromosome))

    #  1. First we handle if a point probability function is supplied as 'index_distribution' variable.
    chrom_length = len(chromosomes[0])

    for chromosome in chromosomes:
        logging.debug("Chromosome:" + str(chromosome))
    if index_distribution:
        index_probabilities = np.asarray([index_distribution(i) for i in range(chrom_length)])
        num_possible_points = np.count_nonzero(index_probabilities)
        if num_possible_points != num_points:
            warnings.warn("Num points was selected but was not possible due to overriding index distribution function.")
            num_points = num_possible_points
        logging.debug("The distribution was: " + str(index_probabilities))
    else:
        index_probabilities = None

    points = sorted(npr.choice(a=range(chrom_length), p=index_probabilities, size=num_points, replace=False))

    logging.debug("Points " + str(points))

    #  2. Now, based on the points (indices) selected, we split *all* chromosomes genotypes supplied.
    split_chroms = list()
    for chromosome in chromosomes:
        chrom_splits = list()
        last_point = 0
        for point in points:
            fragment = chromosome[last_point: point]
            logging.debug("Fragment from point " + str(point) + " was: " + str(fragment))
            chrom_splits.append(fragment)
            last_point = point
        last_part = chromosome[last_point:]
        logging.debug("Fragment from last part: " + str(last_part))
        chrom_splits.append(last_part)

        for i in range(len(chrom_splits)):
            if type(chrom_splits[i] is not list):
                chrom_splits[i] = list(chrom_splits[i])
        split_chroms.append(chrom_splits)

    logging.debug("Split chroms " + str(split_chroms))

    #  3. Now we reconstruct new chromosome genotypes by randomly giving each fragment an ID and joining them by ID.
    num_fragments = len(points) + 1  # Assumption only holds true if a single point isn't selected twice earlier in 1.
    num_chromosomes = len(chromosomes)
    new_genotypes = list()
    frag_ids = list()  # Index is frag id
    for fragment_id in range(num_fragments):
        frag_ids.append(npr.choice(a=range(num_chromosomes), size=num_chromosomes, replace=False))
    logging.debug("All Frag IDS " + str(frag_ids))
    for chromosome_id in range(num_chromosomes):
        new_genotype = list()
        frags = [frag_id[chromosome_id] for frag_id in frag_ids]
        logging.debug("Chromosome " + str(chromosome_id) + " frag IDs: " + str(frags))
        for frag_i in range(len(frags)):
            new_genotype.extend(split_chroms[frags[frag_i]][frag_i])  # This got complicated, can it be revised?

        new_genotypes.append(new_genotype)

    #  4. Create new chromosomes based on crossovers.
    first_chromosome_function = chromosomes[0].chromosome_function
    for chromosome in chromosomes:
        assert(chromosome.chromosome_function == first_chromosome_function)

    offspring = list()
    for i in range(num_chromosomes):
        offspring.append(Chromosome(chromosome_function=first_chromosome_function,
                                    passed_genes=new_genotypes[i]))

    for chromosome in offspring:
        logging.debug("Offspring:" + str(chromosome))
    return offspring


def multiple_crossovers(parent_chromosomes, num_points, chrom_per_crossover, index_distribution=None):
    """
    Crossover two or more (chrom_per_crossover) chromosomes repeatedly, then crossover any remaining and return all
    offspring as a list.
    :param parent_chromosomes:
    A list of chromosomes objects.
    :param num_points:
    The number of points to crossover.
    :param chrom_per_crossover:
    The number of chromosomes to involve in a crossover session.
    :param index_distribution:
    A function which gives a probability of crossover at a given index.
    :return offspring:
    A list of chromosome objects.
    """
    chromosomes = copy.deepcopy(parent_chromosomes)
    number_chromosomes = len(chromosomes)
    leftover = number_chromosomes % chrom_per_crossover

    if leftover is 1:
        leftover = chrom_per_crossover + 1
        number_chromosomes - leftover

    crossovers_to_do = int(number_chromosomes / chrom_per_crossover)
    npr.shuffle(chromosomes)

    offspring = list()
    for i in range(crossovers_to_do):
        chromosome_pool = list()
        for j in range(chrom_per_crossover):
            chromosome_pool.append(chromosomes.pop())

        offspring.extend(point_crossover(chromosomes=chromosome_pool, num_points=num_points,
                                         index_distribution=index_distribution))

    if len(chromosomes) > 0:
        remaining_offspring = point_crossover(chromosomes=chromosomes, num_points=num_points,
                                              index_distribution=index_distribution)
        offspring.extend(remaining_offspring)

    return offspring
