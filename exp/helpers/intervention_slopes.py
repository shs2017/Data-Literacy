import matplotlib.pyplot as plt

class InterventionSlopes:
    def __init__(self):
        self.slopes = {}

    def add_intervention_slope(self, key, ages, log_mortality):
        self.slopes[key] = self._calculate_slope(ages, log_mortality)

    def _calculate_slope(self, ages, log_mortality):
        numerator = log_mortality[-1] - log_mortality[0]
        denominator = ages[-1] - log_mortality[0]
        slope = numerator / denominator
        return slope

    def calculate_best_intervention(self):
        best_intervention = None
        best_slope = None
        
        for intervention, slope in self.slopes.items():
            if best_slope is None or best_slope > slope:
                best_intervention = intervention
                best_slope = slope
        
        return best_intervention
    
    def plot_inverse_slopes(self):
        fig = plt.figure(figsize=(15, 3))

        inverse_sorted_slopes = self._calculate_inverse_sorted_slopes()
        for key, slope in inverse_sorted_slopes.items():
            plt.bar(key, slope)

        plt.xticks(rotation=-90)
        plt.ylabel(f'1 / Slope')
        plt.title('Ranked Interventions (Best to worst)')
        plt.show()

    def _calculate_inverse_sorted_slopes(self):
        inverse_slopes = {key: 1 / slope for key, slope in self.slopes.items()}
        inverse_sorted_slopes = dict(sorted(inverse_slopes.items(), key=lambda item: item[1], reverse=True))
        return inverse_sorted_slopes
