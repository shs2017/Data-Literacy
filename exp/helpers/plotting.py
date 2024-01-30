import matplotlib.pyplot as plt
import numpy as np

from typing import Union

from .gompertz import *

EPS = 1e-7
COLOR_MAP = ["#ADD8E6", "#008000", "#FFD700", "#800080", "#FF7F50", "#40E0D0", "#708090", "#FF8C00", "#FF00FF", "#008080"]


class NoInterventionPlotter:
    def plot(self, dataset: dict, ages: np.array, log_mortality: np.array, key: str) -> None:
        no_intervention_ages = calculate_ages(dataset[key])

        no_intervention_mortality_rate = calculate_mortality_rate(dataset[key])
        no_intervention_log_mortality_rate = np.log(no_intervention_mortality_rate + EPS)

        plt.scatter(no_intervention_ages, no_intervention_log_mortality_rate, label='Observed Data', color=COLOR_MAP[0])
        plt.plot(ages, log_mortality, label='Fit', color=COLOR_MAP[1])
        plt.xlabel('Age of Mice (Years)')
        plt.ylabel(f'Mortality Rate (Control Group)')
        plt.legend()
        plt.show()

class OneInterventionPlotter:
    N_COLUMNS = 2
    N_ROWS = 2
    FIG_SIZE = (15, 10)

    def plot(self, dataset: dict, ages: np.array, log_mortality: dict, keys: str) -> None:
        fig, axis = plt.subplots(self.N_COLUMNS, self.N_ROWS, figsize=self.FIG_SIZE)
        
        for i in range(len(keys) // self.N_COLUMNS):
            for j in range(self.N_COLUMNS):
                intervention_index = self.N_COLUMNS * i + j
        
                # Get the acutal data points
                intervention_key = keys[intervention_index]
                intervention_dataset = dataset[intervention_key]
                intervention_ages = calculate_ages(intervention_dataset)
                intervention_log_mortality_rate = np.log(calculate_mortality_rate(intervention_dataset) + EPS)
                
                # Plot
                axis[i][j].scatter(intervention_ages, intervention_log_mortality_rate, label='Observed Data', color=COLOR_MAP[0])
                axis[i][j].plot(ages, log_mortality[intervention_key], label='All Gompertz Fit', color=COLOR_MAP[1])
                    
                axis[i][j].set_xlabel('Age of Mice (Years)')
                axis[i][j].set_ylabel(f'Mortality Rate ({intervention_key})')
        
        plt.tight_layout()
        plt.show()

class TwoInterventionPlotter:
    FIG_SIZE = (15, 10)
    N_INTERVENTIONS = 4

    def plot(self, dataset: dict, ages: np.array, log_mortality: dict, key: str) -> None:
        fig = plt.figure(figsize=(15, 5))

        interaction_factor_index = 0
        for intervention_key, log_mortality_rate in log_mortality.items():
            color = COLOR_MAP[interaction_factor_index]
            plt.plot(ages, log_mortality_rate, label=intervention_key, color=color)
            interaction_factor_index += 1
    
        plt.title('Two Intervention Mortality Rate')
        plt.xlabel('Age of Mice (Years)')
        plt.ylabel(f'Log Mortality Rate')
        plt.legend()
        plt.show()

class ThreeInterventionPlotter:
    N_COLS = 2
    N_ROWS = 2
    FIG_SIZE = (15, 10)

    def plot(self, dataset: dict, ages: np.array, log_mortality: dict, key: str) -> None:
        fig, axis = plt.subplots(self.N_COLS, self.N_ROWS, figsize=self.FIG_SIZE)
        
        i = 0
        j = 0
        for intervention_key, log_mortality_rate in log_mortality.items():
            intervention_dataset = dataset[intervention_key]
    
            current_ages = calculate_ages(intervention_dataset)
            actual_log_mortality_rate = np.log(calculate_mortality_rate(intervention_dataset) + EPS)
        
            # Plot
            axis[i][j].scatter(current_ages, actual_log_mortality_rate, label='Observed Data', color=COLOR_MAP[0])
            axis[i][j].plot(ages, log_mortality_rate, label='All Gompertz Fit', color=COLOR_MAP[1])
                
            axis[i][j].set_xlabel('Age of Mice (Years)')
            axis[i][j].set_ylabel(f'Mortality Rate ({intervention_key})')

            if j == 1:
                i += 1
                j = 0
            else:
                j += 1

        plt.tight_layout()
        plt.show()

class AllInterventionPlotter:
    def plot(self, dataset: dict, ages: np.array, log_mortality: Union[dict, np.array], key: str) -> None:
        # plt.scatter(all_interventions_ages, log_mortality_rate, label='Observed Data', color=COLOR_MAP[0])
        plt.plot(ages, log_mortality, label='All Gompertz Fit', color=COLOR_MAP[1])
        plt.xlabel('Age of Mice (Years)')
        plt.ylabel(f'Mortality Rate')
        plt.legend()
        plt.show()

class Plotter:
    def __init__(self, dataset: dict, ages: np.array, log_mortality: np.array, keys: str) -> None:
        self.dataset = dataset
        self.ages = ages
        self.log_mortality = log_mortality
        self.keys = keys

    def plot(self, n_interventions):
        plotter = None
        if n_interventions == 0:
            plotter = NoInterventionPlotter()
        elif n_interventions == 1:
            plotter = OneInterventionPlotter()
        elif n_interventions == 2:
            plotter = TwoInterventionPlotter()
        elif n_interventions == 3:
            plotter = ThreeInterventionPlotter()
        elif n_interventions == 4:
            plotter = AllInterventionPlotter()
        else:
            raise ValueError('There cannot be more than 4 interventions')

        plotter.plot(self.dataset, self.ages, self.log_mortality, self.keys)
