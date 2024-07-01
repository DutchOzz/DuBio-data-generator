# DuBio-data-generator

This codebase was used to research caching in probabilistic databases, and is linked to a research paper.

Setting up the database is done using the files:
bddFunctions.py
connection.py
dictFunctions.py
tableDataFunctions.py
tableFunctions.py
config.py

All other files can be run individually.
To do this, first config.py has to be filled in with your database information.

The most important files used to create the research paper were:
showRandomness.py - This runs the calculateProbabilities query x times and shows the variation in execution time
SQ1createFunctions.py - This runs the calculateProbabilities query while varying row count and and fixing all other parameters. It can also be tweaked to run other queries by changing the queries in the runtest() function. Results are stored in SQ1results.txt, and can be analysed using plotData.py
RQ.py - This tests the time taken to run a query while varying one parameter and fixing the rest. Test ranges, fixed values and run amount can be tweaked in RQcreateFunction.py, as RQ.py functions as an interface. In the research paper this file is used to create the figures to answer SQ2. Again, all results are stored, now in results.txt.
RQcompareRandomVariables.py runs the updateDictionary query and the calculateProbabilities queries while randomising database parameters. Results are stored in RQcompareRandomVariables.txt, and can be analysed in RQanalyse.py. In the paper, this is used to create the figures for the final research question.

There are many more files, which are remnants of previous experiments.