import numpy as np
import pandas as pd

from scipy.optimize import curve_fit

from dataclasses import dataclass
from typing import Any


def gompertz(x: Any, alpha: np.float64, beta: np.float64):
    return alpha * np.exp(beta * x)

class Parameters:
    """Stores the alpha and beta parameters of the Gompertz curve
       for all intervention combinations in the dataset"""

    def __init__(self, dataset):
        self.dataset = dataset

        self.alphas = {}
        self.betas = {}

    def compute(self):
        for key, current_dataset in self.dataset.items():
            all_ages = calculate_ages(current_dataset)
            all_mortality_rate = calculate_mortality_rate(current_dataset)
            
            predicted_parameters = fit_gompertz_model(all_ages, all_mortality_rate)
            
            self.alphas[key] = predicted_parameters.alpha
            self.betas[key] = predicted_parameters.beta
        return self

    def __getitem__(self, key):
        return (self.alphas[key], self.betas[key])

    def keys(self):
        return self.alphas.keys()

def compute_alpha_and_beta(dataset):
    """Returns all alpha and beta parameters of the Gompertz curve
       for each intervention combination in the dataset"""

    alpha_parameters = {}
    beta_parameters = {}
    
    for key, current_dataset in dataset.items():
        all_ages = calculate_ages(current_dataset)
        all_mortality_rate = calculate_mortality_rate(current_dataset)
        
        predicted_parameters = fit_gompertz_model(all_ages, all_mortality_rate)
        
        alpha_parameters[key] = predicted_parameters.alpha
        beta_parameters[key] = predicted_parameters.beta
    
    return alpha_parameters, beta_parameters

@dataclass
class GompertzParameters:
    alpha: np.float64
    beta: np.float64

    @staticmethod
    def from_sequence(seq):
        return GompertzParameters(alpha=seq[0], beta=seq[1])

    def to_tuple(self) -> (np.float64, np.float64):
        return (self.alpha, self.beta)

    def __str__(self) -> str:
        return f'(alpha={self.alpha:.4f}, beta={self.beta:.4f})'

    def __repr__(self) -> str:
        return f'(alpha={self.alpha:.4f}, beta={self.beta:.4f})'


DEFAULT_INITIAL_PARAMETERS = GompertzParameters(alpha=0.1, beta=0.085)

def fit_gompertz_model(ages: pd.DataFrame,
                       mortality_rate: pd.DataFrame,
                       initial_parameters: GompertzParameters = DEFAULT_INITIAL_PARAMETERS,
                       max_fit_iterations: int = 50_000) -> GompertzParameters:
    p0 = initial_parameters.to_tuple()
    predicted_parameters, covariance = curve_fit(gompertz, ages, mortality_rate, p0=p0, maxfev=max_fit_iterations)
    return GompertzParameters.from_sequence(predicted_parameters)

def calculate_ages(dataset) -> np.array:
    return np.array(dataset.x) / 365 # ages in years

def calculate_mortality_rate(dataset) -> np.array:
    """Converts a survival rate dataset into a mortality rate dataset"""
    return np.array(1 - dataset.y)
