from pprint import pprint

from CRUD import AnimalShelter
from dashboard_logic import get_rescue_queries


def explain_query(collection, query, query_name):

    print(f"\n--- {query_name} ---")

    results = collection.database.command(
        "explain",
        {
            "find": collection.name,
            "filter": query
        },
        verbosity="executionStats"
    )

    stats = results["executionStats"]

    print("Documents returned:",
          stats["nReturned"])

    print("Documents examined:",
          stats["totalDocsExamined"])

    print("Index keys examined:",
          stats["totalKeysExamined"])

    print("Execution time (ms):",
          stats["executionTimeMillis"])

    print("Query plan:")
    pprint(results["queryPlanner"]["winningPlan"])


def main():

    # Use the same AnimalShelter initialization
    # that your main.py currently uses.
    shelter = AnimalShelter()

    water_query, mountain_query, disaster_query = get_rescue_queries()

    combined_query = {
        "$or": [
            water_query,
            mountain_query,
            disaster_query
        ]
    }

    collection = shelter.dataBase.animals

    # Test each query
    explain_query(collection, {}, "All Records")

    explain_query(collection, water_query, "Water Rescue")

    explain_query(collection, mountain_query, "Mountain Rescue")

    explain_query(collection, disaster_query, "Disaster Rescue")

    explain_query(collection, combined_query, "Combined All Rescue")


if __name__ == "__main__":
    main()