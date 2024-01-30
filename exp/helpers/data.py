import pandas as pd

CATEGORY_COLUMN = 'category'
SEX_COLUMN = 'sex'

CONTROL_GROUP = 'None'
ALL_GROUP = 'All'
ONE_REMOVED_PREFIX = 'no_'


def is_one_removed_intervention(key: str) -> bool:
    """ Returns true if the key is a three intervention one
        (i.e. one removed out of the four interventions) """
    if len(key) < 3:
        return False

    return key[:len(ONE_REMOVED_PREFIX)] == ONE_REMOVED_PREFIX

def convert_one_removed_intervention_key_to_canonical_key(key: str, intervention_list: []) -> []:
    """Converts a one-removed intervention name to it's canonical name
       (e.g. 'No_InterventionA' => 'InterventionB,InterventionC,InterventionD') """
    removed_key = key[len(ONE_REMOVED_PREFIX):]

    removed_intervention_list = []
    for intervention in intervention_list:
        if intervention != removed_key:
            removed_intervention_list.append(intervention)

    return removed_intervention_list

def create_canonical_intervention_key(key: str, intervention_list: []):
    """Converts the default intervention name to its canonical name, which
       is a comma seperated list of the interventions in `key` from
       `intervention_list`"""

    canonical_interventions = None
    
    if key == ALL_GROUP:
        canonical_interventions = intervention_list
    elif key == CONTROL_GROUP:
        canonical_interventions = []
    elif is_one_removed_intervention(key):
        canonical_interventions = convert_one_removed_intervention_key_to_canonical_key(key, intervention_list)
    else:
        canonical_interventions = [key]

    return ','.join(canonical_interventions)


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(
                        path,
                        skiprows=0,
                        sep=',',
                        engine='python',
                        decimal='.',
                        dtype={'x': 'float64', 'y': 'float64'}
            )

def extract_one_intervention_keys(dataset: pd.DataFrame) -> [str]:
    """Returns the list of intervention names where there is only one intervention"""
    categories = dataset[CATEGORY_COLUMN].unique()

    single_interventions = []
    for category in categories:
        if category == ALL_GROUP:
            continue
        elif category == CONTROL_GROUP:
            continue
        elif is_one_removed_intervention(category):
            continue
        else:
            single_interventions.append(category)
    
    return single_interventions

def create_two_intervention_keys(one_interventions: [str]) -> [str]:
    """Returns the list of intervention names where there is only two interventions"""
    two_interventions = []
    for i in range(len(one_interventions)):
        for j in range(i + 1, len(one_interventions)):
            intervention_pair = ','.join([one_interventions[i], one_interventions[j]])
            two_interventions.append(intervention_pair)
    return two_interventions

def extract_three_intervention_keys(dataset: dict) -> [str]:
    """Returns the list of intervention names where there is only three interventions"""
    return [intervention for intervention in dataset.keys() if intervention.count(',') == 2]    

def extract_four_intervention_keys(dataset: dict) -> str:
    """Returns the list of intervention names where there is only four interventions"""
    for intervention in dataset.keys():
        if intervention.count(',') == 3:
            return intervention
    raise ValueError('No four intervention data found')

def create_dataset_mapping(dataset, single_interventions: []) -> dict:
    """Returns the dictionary mapping intervention names to their resp. data
       where `single_interventions` is a list of the singular interventions"""
    dataset_by_category = {}
    for intervention in dataset[CATEGORY_COLUMN].unique():
        key = create_canonical_intervention_key(intervention, single_interventions)
        intervention_indices = dataset[CATEGORY_COLUMN] == intervention
        
        dataset_category = dataset[intervention_indices].copy()
        dataset_category = dataset_category.drop([SEX_COLUMN, CATEGORY_COLUMN], axis=1)

        dataset_by_category[key] = dataset_category

    return dataset_by_category

def load_and_preprocess(dataset_path: str) -> pd.DataFrame:
    dataset = load_csv(dataset_path)
    
    # fixes naming of no Gal-Nav in dataset for preprocessing
    misnamed_no_gal_nav_index = dataset[CATEGORY_COLUMN] == 'no_Gal_Nav'
    dataset.loc[misnamed_no_gal_nav_index, CATEGORY_COLUMN] = 'no_Gal-Nav'

    # fixes naming of no interventions
    misnamed_no_intervention_index = dataset[CATEGORY_COLUMN].isna()
    dataset.loc[misnamed_no_intervention_index, CATEGORY_COLUMN] = CONTROL_GROUP
    
    # remove nan rows, if applicable
    return dataset.dropna()
