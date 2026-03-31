from src.ingestion.dataextract import run_ingestion
from src.transformation.silver import run_silver
from src.modeling.model import run_modeling
from DB.analytics.queries import run_queries

if __name__ == "__main__":
    run_ingestion()
    run_silver()
    run_modeling()
    run_queries()