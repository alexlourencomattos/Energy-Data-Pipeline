import argparse

from DB.analytics.queries import run_queries
from src.ingestion.dataextract import run_ingestion
from src.modeling.model import run_modeling
from src.transformation.silver import run_silver


STAGES = {
    "ingestion": run_ingestion,
    "silver": run_silver,
    "modeling": run_modeling,
    "analytics": run_queries,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Energy Data Pipeline")
    parser.add_argument(
        "--stage",
        choices=["all", *STAGES.keys()],
        default="all",
        help="Run a specific stage or the entire pipeline.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.stage == "all":
        for stage_fn in STAGES.values():
            stage_fn()
    else:
        STAGES[args.stage]()


if __name__ == "__main__":
    main()
