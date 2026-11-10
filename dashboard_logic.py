# This file Contains the Dashboard
# Query and Data-processing Logic

import re
import pandas as pd


# noinspection pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming,pep8-naming
def get_rescue_queries():

    # Define regex patterns
    labRegex = re.compile(".*lab.*", re.IGNORECASE)
    chesaRegex = re.compile(".*chesa.*", re.IGNORECASE)
    newRegex = re.compile(".*newf.*", re.IGNORECASE)
    germanRegex = re.compile(".*german.*", re.IGNORECASE)
    alaskanRegex = re.compile(".*mala.*", re.IGNORECASE)
    oldRegex = re.compile(".*old english.*", re.IGNORECASE)
    huskyRegex = re.compile(".*husk.*", re.IGNORECASE)
    rottRegex = re.compile(".*rott.*", re.IGNORECASE)
    goldenRegex = re.compile(".*golden.*", re.IGNORECASE)
    bloodRegex = re.compile(".*blood.*", re.IGNORECASE)
    doberRegex = re.compile(".*dober.*", re.IGNORECASE)

    # Water Rescue Query
    water_query = {
        "animal_type": "Dog",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": {
            "$gte": 26,
            "$lte": 156
        },
        "$or": [
            {"breed": {"$regex": newRegex}},
            {"breed": {"$regex": chesaRegex}},
            {"breed": {"$regex": labRegex}},
        ]
    }

    # Mountain Rescue Query
    mountain_query = {
        "animal_type": "Dog",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {
            "$gte": 26,
            "$lte": 156
        },
        "$or": [
            {"breed": {"$regex": germanRegex}},
            {"breed": {"$regex": alaskanRegex}},
            {"breed": {"$regex": oldRegex}},
            {"breed": {"$regex": huskyRegex}},
            {"breed": {"$regex": rottRegex}},
        ]
    }

    # Disaster Rescue Query
    disaster_query = {
        "animal_type": "Dog",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {
            "$gte": 20,
            "$lte": 300
        },
        "$or": [
            {"breed": {"$regex": germanRegex}},
            {"breed": {"$regex": goldenRegex}},
            {"breed": {"$regex": bloodRegex}},
            {"breed": {"$regex": doberRegex}},
            {"breed": {"$regex": rottRegex}},
        ]
    }

    return water_query, mountain_query, disaster_query


def get_dashboard_records(shelter, rescue_type):

    water_query, mountain_query, disaster_query = (
        get_rescue_queries()
    )

    # No filter
    if not rescue_type:
        return pd.DataFrame(
            shelter.getRecordCriteria({})
        )

    # Water rescue
    elif rescue_type == "Water":
        return pd.DataFrame(
            shelter.getRecordCriteria(water_query)
        )

    # Mountain rescue
    elif rescue_type == "Mountain":
        return pd.DataFrame(
            shelter.getRecordCriteria(mountain_query)
        )

    # Disaster rescue
    elif rescue_type == "Disaster":
        return pd.DataFrame(
            shelter.getRecordCriteria(disaster_query)
        )

    # All rescue types
    elif rescue_type == "All":

        water_data = pd.DataFrame(
            shelter.getRecordCriteria(water_query)
        )

        mountain_data = pd.DataFrame(
            shelter.getRecordCriteria(mountain_query)
        )

        disaster_data = pd.DataFrame(
            shelter.getRecordCriteria(disaster_query)
        )

        combined_data = pd.concat([
            water_data,
            mountain_data,
            disaster_data
        ])

        combined_data = combined_data.drop_duplicates()

        return combined_data

    # Reset
    elif rescue_type == "Reset":
        return pd.DataFrame(
            shelter.getRecordCriteria({})
        )

    return pd.DataFrame()