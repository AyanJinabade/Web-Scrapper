from scraper.scraper_bs4 import scrape_multiple_pages
from scraper.scraper_selenium import scrape_dynamic
from processing.clean_data import clean_data
from storage.save_csv import save_to_csv
from storage.save_sql import save_to_sql
from utils.logger import setup_logger

import logging
import os


def run_pipeline():
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("🚀 Pipeline started")

    try:
        logger.info("Scraping static data...")
        data_static = scrape_multiple_pages() or []

        logger.info("Scraping dynamic data...")
        data_dynamic = scrape_dynamic() or []

        # Combine
        all_data = data_static + data_dynamic
        logger.info(f"Total records scraped: {len(all_data)}")

        if not all_data:
            logger.warning(" No data scraped. Exiting pipeline.")
            return

        logger.info("Cleaning data...")
        df = clean_data(all_data)

        if df is None or df.empty:
            logger.warning("⚠️ DataFrame is empty after cleaning. Exiting.")
            return

        logger.info(f"Cleaned data shape: {df.shape}")

        if "id" in df.columns:
            df = df.drop_duplicates(subset=["id"])
        else:
            df = df.drop_duplicates()

        logger.info(f"After deduplication: {df.shape}")


        # Ensure directory exists
        output_path = "data/processed/quotes.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        logger.info("Saving to CSV...")
        save_to_csv(df, output_path)

        # Save to SQL with safety
        logger.info("Saving to SQL...")
        try:
            save_to_sql(df)
        except Exception as sql_error:
            logger.error(f"❌ SQL save failed: {sql_error}")

        logger.info(" Pipeline completed successfully")

    except Exception as e:
        logger.exception(f"❌ Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()
