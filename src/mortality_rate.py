import numpy as np

from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .gompertz import *

EPS = 1e-7


@dataclass
class MortalityRateArguments:
    parameters: Parameters
    dataset: Any
    intervention_keys: Any
    interaction_factors: Any
    evaluation_ages: Any
    one_intervention_mortality: Any


class MortalityRate:
    def __init__(self, values):
        self.values = values

    def value(self):
        return self.values

    def log(self):
        if isinstance(self.values, dict):
            return {key: np.log(value) for key, value in self.values.items()}
        
        return np.log(self.values + EPS)


class NoInterventionMortalityRate:
    def __init__(self, arguments: MortalityRateArguments):
        no_intervention_ages = calculate_ages(arguments.dataset[arguments.intervention_keys])
        no_intervention_mortality_rate = calculate_mortality_rate(arguments.dataset[arguments.intervention_keys])

        predicted_parameters = fit_gompertz_model(no_intervention_ages, no_intervention_mortality_rate)
        predicted_mortality = gompertz(arguments.evaluation_ages, predicted_parameters.alpha, predicted_parameters.beta)
        self.mortality_rate = MortalityRate(predicted_mortality)


def compute_mortality_per_intervention(arguments: MortalityRateArguments):
    mortality = []

    for key in arguments.intervention_keys:
        mortality_rate = calculate_mortality_rate(arguments.dataset[key].copy())
        alpha, beta = arguments.parameters[key]
        mortality.append(gompertz(arguments.evaluation_ages, alpha, beta))
    return mortality


def compute_actual_mortalities(dataset, ages):
    parameters = Parameters(dataset.copy()).compute()

    mortality = {}
    for key in parameters.keys():
        alpha, beta = parameters[key]
        mortality[key] = gompertz(ages, alpha, beta)

    return mortality


class OneInterventionsMortalityRate:
    def __init__(self, arguments: MortalityRateArguments):
        one_interventions_mortality = compute_mortality_per_intervention(arguments)

        mortality_rates = {}
        for key, mortality_rate in zip(arguments.intervention_keys, one_interventions_mortality):
            mortality_rates[key] = mortality_rate

        self.mortality_rate = MortalityRate(mortality_rates)


class TwoInterventionsMortalityRate:

    def __init__(self, arguments: MortalityRateArguments):
        n_single_iterations = len(arguments.one_intervention_mortality)

        interaction_factor_index = 0
        mortality_rates = {}
        for i in range(n_single_iterations):
            for j in range(i + 1, n_single_iterations):
                interaction_factor = np.array([factor[interaction_factor_index] for factor in arguments.interaction_factors.to_numpy()])
                key = arguments.intervention_keys[interaction_factor_index]
                single_intervention_contributions = arguments.one_intervention_mortality[i] + arguments.one_intervention_mortality[j]
                mortality_rates[key] = single_intervention_contributions + interaction_factor
    
                interaction_factor_index += 1
        
        self.mortality_rate = MortalityRate(mortality_rates)


class ThreeInterventionsMortalityRate:
    INTERVENTION_INDICES = np.array([
                [0, 1, 3],
                [0, 2, 4],
                [1, 2, 5],
                [3, 4, 5]
    ])

    def __init__(self, arguments: MortalityRateArguments):
        alpha_parameters, beta_parameters = compute_alpha_and_beta(arguments.dataset)
        three_interventions_mortality = compute_mortality_per_intervention(arguments)
        
        interactions = self._compute_interventions_interactions(arguments.interaction_factors)
        interventions = self._compute_single_intervention_contributions(arguments.one_intervention_mortality)
        three_interventions_mortality = interactions + interventions
        mortality_rate = self._compute_mortality_rate(three_interventions_mortality, arguments.intervention_keys)
        self.mortality_rate = MortalityRate(mortality_rate)
    
    def _compute_interventions_interactions(self, interaction_factors):
        interaction_factors = interaction_factors.to_numpy()
    
        interactions = []
        for indices in self.INTERVENTION_INDICES:
            interaction = sum([interaction_factors[:, index] for index in indices])
            interactions.append(interaction)
    
        return np.array(interactions)
    
    def _compute_single_intervention_contributions(self, one_interventions_mortality):
        intervention_matrix = np.array(one_interventions_mortality)
    
        three_intervention_indices = list(combinations(range(4), 3))
    
        single_interventions = []
        for indices in three_intervention_indices:
            intervention_sum = 0
            for index in indices:
                intervention_sum += intervention_matrix[index]
            
            single_interventions.append(intervention_sum)
    
        return np.array(single_interventions)

    def _compute_mortality_rate(self, mortality_rate, keys):
        mortality_rates_map = {}
        for intervention_index in range(len(mortality_rate)):
            mortality_rates_map[keys[intervention_index]] = mortality_rate[intervention_index]
        return mortality_rates_map



class AllInterventionsMortalityRate:
    def __init__(self, arguments: MortalityRateArguments):
        interventions = np.array(arguments.one_intervention_mortality).sum(axis=0)
        interactions = np.array(arguments.interaction_factors.to_numpy()).sum(axis=1)
        mortality_rate = interactions + interventions
        self.mortality_rate = MortalityRate(mortality_rate)


class MortalityRateFactory:
    def __init__(self, n_interventions):
        self.n_interventions = n_interventions

    def create(self, arguments: MortalityRateArguments):
        if self.n_interventions == 0:
            return NoInterventionMortalityRate(arguments)
        elif self.n_interventions == 1:
            return OneInterventionsMortalityRate(arguments)
        elif self.n_interventions == 2:
            return TwoInterventionsMortalityRate(arguments)
        elif self.n_interventions == 3:
            return ThreeInterventionsMortalityRate(arguments)
        elif self.n_interventions == 4:
            return AllInterventionsMortalityRate(arguments)
        else:
            raise ValueError('There cannot be more than four interventions')


def compute_mortality_by_n_interventions(dataset, ages, parameters, intervention_keys):
    mortality = []
    for key in intervention_keys:
        mortality_rate = calculate_mortality_rate(dataset[key])
        
        alpha, beta = parameters[key]
        
        mortality.append(gompertz(ages, alpha, beta))
    
    return mortality
