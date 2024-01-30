<h1 align="center"> Predicting most Efficient Interventions for Life Span Increase</h1>

<table>
  <tr>
    <td>
      <img src="fig/2401_sanity_check_male_final.svg" alt="RMR Male Plot">
    </td>
    <td>
      <img src="fig/2401_sanity_check_female_final.svg" alt="Second Image">
    </td>
  </tr>
</table>

This repository contains the code which was used for the
Data Literacy Paper Project "Predicting most Efficient
Interventions for Life Span Increase".

## Abstract
We used data from the ongoing [Robust Mouse Rejuvination (RMR)](https://www.levf.org/projects/robust-mouse-rejuvenation-study-1)
study to predict the effects of multiple
interventions on the lifespan of mice. We analyzed
how each intervention influenced the lifespan
and tried to identify combinations that could
yield the most substantial longevity increase. By
forecasting which factors are pivotal for a noteworthy
increase in lifespan, we aim to pinpoint
combinations worthy of further exploration. We
used the latest data from the intervention study
before its conclusion. We created a linear model
and a multilayer perceptron to predict the expected
mortality rate and therefore the expected
life expectancy given a set of treatments. We
conclude that the multiplayer perceptron gives a
more precise prediction, and based on our analysis,
we recommend conducting additional investigations
involving the combination of rapamycin
and mTERT.


---
## Directory Structure
- **dat** contains data files. The data from *final_datasets* was used for the analysis 
- **exp** contains the python notebooks for our analysis.
- **fig** contains the figures used for the analysis and the paper.
- **src** contains source code that we used for multiple notebooks. 

## Experiments
| Experiment                   | Description                                                                                                                                         |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| 001_GompertzAssumption       | Giving evidence to the assumption that the mortality rates of mice fit to the Gompertz-Makeham Law of Mortality. <br>Reproduction for the Figure 1. |
| 002_ExtractingPointsFromPlot | Preprocessing of the manual elicited data points from the RMR reports. <br>Reproduction for the Figures in the README.md.                           |
| 003_MotivationalAnalysis     | We show that there has been a strong increase in scientific publications on the topic of ageing, particularly since 2015.                           |
| 004_SecondOrderModel   | Here we created a linear model with interaction terms to predict the best intervention combinations.                                                |
| 005_MLPModel             | Here we created a MLP model to predict the best intervention combinations. <br>Reproduction for the Figures 2, 3 and 4.                             |

[//]: # (TODO: Add which experiment produced which Figure. Add to each experiment description "<br>Reproduction for Figure X." if it contributes to one of the shown figures in the paper)
