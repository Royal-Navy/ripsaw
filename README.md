# Project RIPSAW

RIPSAW is a library of code for applying evolutionary algorithms on external applications. Originally it was used by the Maritime Warfare Centre and DSTL as a way to experiment with model-specific optimisation problems such as entity behavioral scripting and parameter optimisation.

The project title isn't an acronym; it's based on the Ripsaw Catfish. The Maritime Warfare Centre's project's are usually named after wild animals.

## How It Works
Modelled around traditional genetic algorithms, RIPSAW uses describes Genes as Python Objects which have a String value.

Chromosomes contain a list of Genes which deployed to an instance of a model called a Wrapper.

User supplied logging functions can be used to extract specific data from wrappers after their runtime execution has finished.

An optimiser will iteratively run epochs as described below.

Logs are available of individual chromosome performance on completion of the first epoch and are updated every epoch. 

### An Epoch:
1. Wrappers are created for every Chromosome that has not been evaluated for a score.

2. Each Chromosome has it's gene's String values written into a definable region of a text file.

3. The Wrapper is executed.

4. An output score is assigned to the Chromosome based on a user's supplied function. 

5. A log value from the wrapper is returned based on a user's supplied function.

6. The optimiser will select chromosomes based on their performance for producing offspring. 

7. Offspring (a list of new chromosomes) are created by the process of Crossover(s).

8. Selected offspring replace the lowest scoring chromosomes from the previous iteration.

9. The optimsiser may mutate (completely randomise) some Chromosomes or Genes at random.

10. When some stopping criteria is met by the optimiser - such as maximum allowed execution time, the optimiser will stop.

## Getting Started
For examples of code in use, the Genetics and Wrapper tests should show examples of all of the following. The Optimiser test is an example of a full RIPSAW configration and execution.

### Data Structures
Chromosomes and Genes are essential data structures supplied by the user to RIPSAW:
* Users define custom Gene objects as a Python object.

* Chromosomes are defined as having genotype functions. 

Genotype, Output, Execution and Log dictionaries are parameters that are currently generated by a function in the assumptions module. As the program and user-base matures, these will be migrated out as explicit paramerisation for the user. The dictionary generator is treated as a mildly convienient abstraction for now.

### Functions
User Supplied functions are supplied to RIPSAW by the user to configure, optimise and get output from RIPSAW.

* #### Chromosome Functions
Chromosome functions describe the genotype of a given Chromosome. They should return a list of Genes.

* #### Logging Functions
Logging functions gather the output of a Chromosome and it's wrapper. They should return a list of Strings, of which are comma delimited into the logs in a deterministic sequence.

* #### Scoring Functions
Scoring functions are used by the optimiser to make selections during the evolutionary process. They should return a Float or Integer.

### Parameters
Parameter configuration is a core part of optimisation problems. 

* #### Optimiser Parameters such as the mutation rate, number of crossovers per epoch and number of Chromosomes in the optimiser are configurable. A user should look for guidance in other resources as how to intuitively set these.

* #### Wrapper configuration such as template location, relative executable path, output files and more need to be set.

## Wrappers
RIPSAW Wraps External Applications for Python by using environment wrappers.

The three primary steps are:
1.  Write some data to input files based on genes.
2.  Execute an external program.
3.  Read the output files with a user-supplied function to establish a score.

Wrappers can be executed in parallel and use Python's Multiprocessing to do so.

Wrapped scenarios need to have a template created for them with a region identifier for where the genes are to be written. A template is normally a folder with an executable in it.

## License
The license can be found in the LICENSE file in the root directory.
