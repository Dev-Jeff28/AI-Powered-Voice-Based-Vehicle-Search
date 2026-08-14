import json
from pathlib import Path

from app.models.searchQuery import SearchQuery
from app.repositories.repository import Repository
from app.services.search import SearchService
from app.memory.memory import Memory


TRUCK_TYPES = [
    "mini truck",
    "light truck",
    "medium truck",
    "heavy truck"
]


FIELDS = [
    "brand",
    "model",
    "year",
    "usage",
    "price",
    "city",
    "body_type",
    "fuel_type"
]


class DummyResponseService:

    def respond(
        self,
        vehicles,
        search_query
    ):
        return {
            "vehicles": vehicles,
            "search_query": search_query,
            "assistant_response": ""
        }


class DummyMemory:

    def __init__(self):
        self.data = {}

    def get(self, session_id):

        if session_id not in self.data:

            class ConversationMemory:
                pass

            self.data[session_id] = ConversationMemory()

        return self.data[session_id]

    def update(
        self,
        session_id,
        memory
    ):
        self.data[session_id] = memory


def load_test_cases():

    path = (
        Path(__file__).parent
        / "search_cases.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def build_query(
    search_query
):

    body_types = None

    if search_query.body_type is not None:

        if search_query.body_type.lower() == "truck":

            body_types = TRUCK_TYPES

        else:

            body_types = [
                search_query.body_type
            ]

    return body_types


def vehicle_matches_query(
    vehicle,
    search_query
):

    # Brand
    if search_query.brand is not None:

        if (
            vehicle.brand.lower()
            != search_query.brand.lower()
        ):
            return False

    # Model
    if search_query.model is not None:

        if (
            vehicle.model.lower()
            != search_query.model.lower()
        ):
            return False

    # Year
    if search_query.year is not None:

        if vehicle.year != search_query.year:
            return False

    # Usage
    if search_query.usage is not None:

        if (
            vehicle.usage.lower()
            != search_query.usage.lower()
        ):
            return False

    # Price
    if search_query.price is not None:

        if vehicle.price > search_query.price:
            return False

    # City
    if search_query.city is not None:

        if (
            vehicle.city.lower()
            != search_query.city.lower()
        ):
            return False

    # Body type
    if search_query.body_type is not None:

        if search_query.body_type.lower() == "truck":

            if (
                vehicle.body_type.lower()
                not in TRUCK_TYPES
            ):
                return False

        else:

            if (
                vehicle.body_type.lower()
                != search_query.body_type.lower()
            ):
                return False

    # Fuel type
    if search_query.fuel_type is not None:

        if (
            vehicle.fuel_type.lower()
            != search_query.fuel_type.lower()
        ):
            return False

    return True


def calculate_score(
    vehicle,
    search_query
):

    exact_match_score = 0
    distance = 0

    # Brand
    if search_query.brand is not None:

        if (
            vehicle.brand.lower()
            == search_query.brand.lower()
        ):
            exact_match_score += 1

    # Model
    if search_query.model is not None:

        if (
            vehicle.model.lower()
            == search_query.model.lower()
        ):
            exact_match_score += 1

    # Year
    if search_query.year is not None:

        if vehicle.year == search_query.year:
            exact_match_score += 1

        distance += abs(
            vehicle.year
            - search_query.year
        )

    # Usage
    if search_query.usage is not None:

        if (
            vehicle.usage.lower()
            == search_query.usage.lower()
        ):
            exact_match_score += 1

    # Price
    if search_query.price is not None:

        distance += abs(
            vehicle.price
            - search_query.price
        )

    # City
    if search_query.city is not None:

        if (
            vehicle.city.lower()
            == search_query.city.lower()
        ):
            exact_match_score += 1

    # Body type
    if search_query.body_type is not None:

        if search_query.body_type.lower() == "truck":

            if (
                vehicle.body_type.lower()
                in TRUCK_TYPES
            ):
                exact_match_score += 1

        elif (
            vehicle.body_type.lower()
            == search_query.body_type.lower()
        ):
            exact_match_score += 1

    # Fuel type
    if search_query.fuel_type is not None:

        if (
            vehicle.fuel_type.lower()
            == search_query.fuel_type.lower()
        ):
            exact_match_score += 1

    return (
        exact_match_score,
        distance
    )


def calculate_expected_ranking(
    vehicles,
    search_query
):

    ranked = []

    for vehicle in vehicles:

        score, distance = calculate_score(
            vehicle,
            search_query
        )

        ranked.append(
            (
                vehicle,
                score,
                distance
            )
        )

    ranked.sort(
        key=lambda item: (
            -item[1],
            item[2]
        )
    )

    return ranked


def print_vehicle(
    vehicle
):

    return (
        f"ID: {vehicle.id} | "
        f"{vehicle.brand} "
        f"{vehicle.model} | "
        f"Year: {vehicle.year} | "
        f"Price: ₹{vehicle.price} | "
        f"City: {vehicle.city} | "
        f"Body: {vehicle.body_type}"
    )


def evaluate():

    test_cases = load_test_cases()

    repository = Repository()

    response_service = (
        DummyResponseService()
    )

    memory = DummyMemory()

    search_service = SearchService(
        repository,
        response_service,
        memory
    )

    total_cases = len(test_cases)

    filter_passes = 0
    no_result_passes = 0
    ranking_passes = 0

    total_relevant = 0
    total_returned = 0
    total_valid_returned = 0

    recall_values = []

    print()
    print("=" * 75)
    print("DEEP SEARCH EVALUATION")
    print("=" * 75)
    print()

    for index, test_case in enumerate(
        test_cases,
        start=1
    ):

        name = test_case["name"]

        search_query = SearchQuery(
            **test_case["query"]
        )

        print(
            f"Test {index}/{total_cases}"
        )

        print(
            f"Query: {name}"
        )

        print(
            f"SearchQuery: {search_query}"
        )

        # -------------------------------------------------
        # Get complete matching set directly from repository
        # -------------------------------------------------

        body_types = build_query(
            search_query
        )

        all_matching_vehicles = (
            repository.search(
                search_query,
                body_types
            )
        )

        # -------------------------------------------------
        # Run actual SearchService
        # -------------------------------------------------

        response = search_service.search(
            search_query,
            "evaluation-session"
        )

        returned_vehicles = response[
            "vehicles"
        ]

        # -------------------------------------------------
        # 1. FILTER CORRECTNESS
        # -------------------------------------------------

        invalid_vehicles = []

        for vehicle in returned_vehicles:

            if not vehicle_matches_query(
                vehicle,
                search_query
            ):

                invalid_vehicles.append(
                    vehicle
                )

        filter_correct = (
            len(invalid_vehicles) == 0
        )

        if filter_correct:

            filter_passes += 1

            print(
                "Filter correctness: PASS ✓"
            )

        else:

            print(
                "Filter correctness: FAIL ✗"
            )

            for vehicle in invalid_vehicles:

                print(
                    "  INVALID:",
                    print_vehicle(vehicle)
                )

        # -------------------------------------------------
        # 2. NO-RESULT CORRECTNESS
        # -------------------------------------------------

        expected_count = len(
            all_matching_vehicles
        )

        actual_count = len(
            returned_vehicles
        )

        if expected_count == 0:

            no_result_correct = (
                actual_count == 0
            )

            if no_result_correct:

                no_result_passes += 1

                print(
                    "No-result correctness: PASS ✓"
                )

            else:

                print(
                    "No-result correctness: FAIL ✗"
                )

        else:

            print(
                "No-result correctness: N/A "
                f"({expected_count} matching vehicles)"
            )

        # -------------------------------------------------
        # 3. RANKING CORRECTNESS
        # -------------------------------------------------

        expected_ranking = (
            calculate_expected_ranking(
                all_matching_vehicles,
                search_query
            )
        )

        expected_top_3 = [
            item[0]
            for item in expected_ranking[:3]
        ]

        expected_ids = [
            vehicle.id
            for vehicle in expected_top_3
        ]

        actual_ids = [
            vehicle.id
            for vehicle in returned_vehicles
        ]

        ranking_correct = (
            actual_ids == expected_ids
        )

        if ranking_correct:

            ranking_passes += 1

            print(
                "Top-3 ranking: PASS ✓"
            )

        else:

            print(
                "Top-3 ranking: FAIL ✗"
            )

            print(
                "Expected ranking:"
            )

            for vehicle in expected_top_3:

                score, distance = (
                    calculate_score(
                        vehicle,
                        search_query
                    )
                )

                print(
                    f"  {print_vehicle(vehicle)} "
                    f"| score={score} "
                    f"| distance={distance}"
                )

            print(
                "Actual ranking:"
            )

            for vehicle in returned_vehicles:

                score, distance = (
                    calculate_score(
                        vehicle,
                        search_query
                    )
                )

                print(
                    f"  {print_vehicle(vehicle)} "
                    f"| score={score} "
                    f"| distance={distance}"
                )

        # -------------------------------------------------
        # 4. RECALL@3
        # -------------------------------------------------

        relevant_count = len(
            all_matching_vehicles
        )

        relevant_ids = {
            vehicle.id
            for vehicle in all_matching_vehicles
        }

        returned_relevant = sum(
            1
            for vehicle in returned_vehicles
            if vehicle.id in relevant_ids
        )

        if relevant_count > 0:

            recall_at_3 = (
                returned_relevant
                / min(relevant_count, 3)
                * 100
            )

            recall_values.append(
                recall_at_3
            )

            print(
                f"Recall@3: "
                f"{recall_at_3:.2f}% "
                f"({returned_relevant}/"
                f"{min(relevant_count, 3)})"
            )

        else:

            print(
                "Recall@3: N/A "
                "(no relevant vehicles)"
            )

        total_relevant += relevant_count
        total_returned += actual_count
        total_valid_returned += (
            len(returned_vehicles)
            - len(invalid_vehicles)
        )

        print(
            f"Complete matching set: "
            f"{relevant_count}"
        )

        print(
            f"Returned by SearchService: "
            f"{actual_count}"
        )

        print(
            "Returned vehicles:"
        )

        if not returned_vehicles:

            print(
                "  No vehicles"
            )

        else:

            for vehicle in returned_vehicles:

                print(
                    " ",
                    print_vehicle(vehicle)
                )

        print(
            "-" * 75
        )

    # -----------------------------------------------------
    # FINAL RESULTS
    # -----------------------------------------------------

    filter_accuracy = (
        filter_passes
        / total_cases
        * 100
    )

    ranking_accuracy = (
        ranking_passes
        / total_cases
        * 100
    )

    average_recall = (
        sum(recall_values)
        / len(recall_values)
        if recall_values
        else 0
    )

    print()
    print("=" * 75)
    print("FINAL RESULTS")
    print("=" * 75)

    print(
        f"Total queries:              "
        f"{total_cases}"
    )

    print(
        f"Filter correctness:        "
        f"{filter_accuracy:.2f}%"
    )

    print(
        f"Ranking correctness:       "
        f"{ranking_accuracy:.2f}%"
    )

    print(
        f"No-result tests passed:    "
        f"{no_result_passes}"
    )

    print(
        f"Total relevant vehicles:   "
        f"{total_relevant}"
    )

    print(
        f"Total returned vehicles:   "
        f"{total_returned}"
    )

    print(
        f"Average Recall@3:          "
        f"{average_recall:.2f}%"
    )

    print("=" * 75)


if __name__ == "__main__":
    evaluate()