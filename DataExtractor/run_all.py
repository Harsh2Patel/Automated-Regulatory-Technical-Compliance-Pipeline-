import time
from pipeline_main import run_pipeline
from generate_report import create_markdown_report


def main():
    print("=" * 50)
    print("🚀 LAUNCHING COMPLIANCE DATA PIPELINE SYSTEM")
    print("=" * 50)

    # Step 1: Fetch and update the database
    start_time = time.time()
    run_pipeline()

    # Step 2: Generate the human-readable summary report
    create_markdown_report()

    end_time = time.time()
    elapsed = end_time - start_time

    print("=" * 50)
    print(f"✅ SUCCESS: System update finished in {elapsed:.2f} seconds.")
    print("=" * 50)


if __name__ == "__main__":
    main()