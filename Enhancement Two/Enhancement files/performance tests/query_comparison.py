#########################################
# Query Comparison Test
########################################

# Page imports
import json
import time
from collections import Counter
from statistics import median, mean
import pandas as pd
from CRUD import AnimalShelter
from dashboard_logic import get_rescue_queries


# Number of measured comparisons
RUNS = 20

###############################################
# Original "ALL" query method
##############################################

def original_approach(shelter, water_query, mountain_query, disaster_query):

    water_data = pd.DataFrame(
        shelter.getRecordCriteria(water_query)
    )

    mountain_data = pd.DataFrame(
        shelter.getRecordCriteria(mountain_query)
    )

    disaster_data = pd.DataFrame(
        shelter.getRecordCriteria(disaster_query)
    )

    combined_data = pd.concat(
        [water_data, mountain_data, disaster_data]
    )

    combined_data = combined_data.drop_duplicates()

    return combined_data.to_dict("records")

###############################################
# Revised Query Method using $or filter
##############################################

def combined_approach(shelter, combined_query):

    combined_data = pd.DataFrame(
        shelter.getRecordCriteria(combined_query)
    )

    return combined_data.to_dict("records")

# Convert records into comparable strings.
def normalize_records(records):

    return Counter(
        json.dumps(record, sort_keys=True, default=str)
        for record in records
    )

def main():

    shelter = AnimalShelter()

    try:
        # Get the original rescue queries
        water_query, mountain_query, disaster_query = get_rescue_queries()

        # Build the combined query
        combined_query = {
            "$or": [
                water_query,
                mountain_query,
                disaster_query
            ]
        }

        original_times = []
        combined_times = []

        original_records = None
        combined_records = None

        # Warm-up runs (not included in measurements)
        print("\nWarming up both approaches...")

        original_approach(
            shelter, water_query, mountain_query, disaster_query
        )

        combined_approach(shelter, combined_query)

        print("Warm-up complete.")

        print(f"\nRunning {RUNS} measured comparisons...")

        # Run 20 comparisons, alternating execution order
        for run in range(RUNS):

            if run % 2 == 0:
                # Even-numbered runs: Original first

                start_time = time.perf_counter()

                current_original = original_approach(
                    shelter,
                    water_query,
                    mountain_query,
                    disaster_query
                )

                original_elapsed = time.perf_counter() - start_time

                start_time = time.perf_counter()

                current_combined = combined_approach(
                    shelter, combined_query
                )

                combined_elapsed = time.perf_counter() - start_time

            else:
                # Odd-numbered runs: Combined first

                start_time = time.perf_counter()

                current_combined = combined_approach(
                    shelter, combined_query
                )

                combined_elapsed = time.perf_counter() - start_time

                start_time = time.perf_counter()

                current_original = original_approach(
                    shelter,
                    water_query,
                    mountain_query,
                    disaster_query
                )

                original_elapsed = time.perf_counter() - start_time

            # Save execution times in milliseconds
            original_times.append(original_elapsed * 1000)
            combined_times.append(combined_elapsed * 1000)

            # Save the first run's records for comparison
            if run == 0:
                original_records = current_original
                combined_records = current_combined

            # Verify that results remain consistent across runs
            if normalize_records(current_original) != normalize_records(original_records):
                print(f"WARNING: Original results changed during run {run + 1}.")

            if normalize_records(current_combined) != normalize_records(combined_records):
                print(f"WARNING: Combined results changed during run {run + 1}.")

            print(
                f"Run {run + 1:02d}: "
                f"Original = {original_elapsed * 1000:.3f} ms | "
                f"Combined = {combined_elapsed * 1000:.3f} ms"
            )

        # Compare the actual animal records
        original_normalized = normalize_records(original_records)
        combined_normalized = normalize_records(combined_records)

        print("\n--- Record Comparison ---")
        print("Original records:", len(original_records))
        print("Combined records:", len(combined_records))

        if original_normalized == combined_normalized:
            print("RESULT: Both approaches returned identical records.")
        else:
            print("RESULT: The approaches returned different records.")

            missing = original_normalized - combined_normalized
            extra = combined_normalized - original_normalized

            print("\nRecords missing from combined approach:")
            for record, count in missing.items():
                print(json.loads(record), "Count:", count)

            print("\nAdditional records in combined approach:")
            for record, count in extra.items():
                print(json.loads(record), "Count:", count)

        # Calculate performance statistics
        original_median = median(original_times)
        combined_median = median(combined_times)

        original_average = mean(original_times)
        combined_average = mean(combined_times)

        print("\n--- Performance Summary ---")
        print(f"Number of measured runs: {RUNS}")

        print("\nOriginal approach:")
        print(f"Median:   {original_median:.3f} ms")
        print(f"Average:  {original_average:.3f} ms")
        print(f"Minimum:  {min(original_times):.3f} ms")
        print(f"Maximum:  {max(original_times):.3f} ms")

        print("\nCombined approach:")
        print(f"Median:   {combined_median:.3f} ms")
        print(f"Average:  {combined_average:.3f} ms")
        print(f"Minimum:  {min(combined_times):.3f} ms")
        print(f"Maximum:  {max(combined_times):.3f} ms")

        # Calculate percentage improvement using median times
        if original_median > 0:
            improvement = (
                (original_median - combined_median)
                / original_median
            ) * 100

            print("\n--- Performance Improvement ---")

            if improvement > 0:
                print(f"Combined approach was {improvement:.2f}% faster.")
            elif improvement < 0:
                print(f"Combined approach was {abs(improvement):.2f}% slower.")
            else:
                print("Both approaches had the same median execution time.")

    finally:
        shelter.client.close()


if __name__ == "__main__":
    main()
