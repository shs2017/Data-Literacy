import numpy as np

from itertools import combinations


class InteractionFactors:
    # Here we have the linear model
    # the (i, j) entry being one in a row
    # represents the (i, j) factor
    # being included.
    #
    # e.g. the first row has factors
    # i_12 + i_13 + i_23
    #
    # the columns represent factors:
    # (1,2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)
    LINEAR_MODEL = np.array([
                [1, 1, 0, 1, 0, 0],
                [1, 0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0, 1],
                [0, 0, 0, 1, 1, 1],
    ])

    def __init__(self, one_interventions_mortality, three_interventions_mortality):
        self.one_interventions_mortality = one_interventions_mortality
        self.three_interventions_mortality = three_interventions_mortality

        self.interaction_factors = np.array([])

    def calculate(self):
        diffs = self._compute_intervention_differences()
    
        inverse_linear_model = np.linalg.pinv(self.LINEAR_MODEL)
        
        interaction_factors = []
        for time_step in range(len(diffs[0])):
            current_time_step_diff = np.array(list([diff[time_step] for diff in diffs]))
            time_step_interaction_factors = inverse_linear_model @ current_time_step_diff
            interaction_factors.append(time_step_interaction_factors)
        
        self.interaction_factors = np.array(interaction_factors)

    def _compute_intervention_differences(self):
        """
        Here we compute the different between the predicted mortality rates of three interventions
        and the individual interventions mortality rates that make up the three interventions
        """
        three_intervention_indices = list(combinations(range(4), 3))
    
        diffs = []
        for i in range(len(three_intervention_indices)):
            diff = self.three_interventions_mortality[i]
            for index in three_intervention_indices[i]:
                diff -= np.array(self.one_interventions_mortality[index])
            diffs.append(diff)
    
        return diffs

    def to_numpy(self):
        return self.interaction_factors
