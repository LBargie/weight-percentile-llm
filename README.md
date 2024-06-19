# Calculating child weight percentiles with LLMs

This LLM example uses data from the World Health Organization (WHO) for child growth standards to calculate weight percentiles.

You can tell the LLM the gender, weight and age of the child and the LLM will first convert the age to days then write a SQL query that calculates the percentile based on the WHO data stored in the DuckDB database.

This is similar to an earlier project of [mine](https://github.com/LBargie/child-growth-charts) but replaces the web app with an LLM.

This project, as well as the previous one, was inspired by the "red book" that accompanies your child after their birth and the weight recordings that are made in it.

## Set-up

The set-up and required packages is the same as my [data-talk](https://github.com/LBargie/data-talk) repo. 
