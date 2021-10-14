[![coverage report](https://gitlab.com/maritime-warfare-centre/ripsaw/badges/master/coverage.svg)](https://gitlab.com/maritime-warfare-centre/ripsaw/-/commits/master)
[![pipeline status](https://gitlab.com/maritime-warfare-centre/ripsaw/badges/master/pipeline.svg)](https://gitlab.com/maritime-warfare-centre/ripsaw/-/commits/master)


# RIPSAW

RIPSAW is a library of code for applying evolutionary algorithms on external applications. 

## Genetics
There is a directory of useful genetic functions including:
*  Crossovers
*  Selection
*  Genotype (standard RIPSAW objects)
*  Optimisers

## Wrapper
RIPSAW Wraps External Applications (such as simulations) for Python by using environment wrappers.

The three primary steps are:
1.  Write some data to input files.
2.  Use an external program.
3.  Read the output files with a function to establish a score.

## License
The license can be found in the LICENSE file in the root directory.
