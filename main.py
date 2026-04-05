from scraper.scraper_bs4 import scrape_multiple_pages
from scraper.scraper_selenium import scrape_dynamic
from processing.clean_data import clean_data
from storage.save_csv import save_to_csv
from storage.save_sql import save_to_sql
from utils.logger import setup_logger

import logging


def run_pipeline():
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("🚀 Pipeline started")

    try:
        # -------- SCRAPING --------
        logger.info("Scraping static data...")
        data_static = scrape_multiple_pages()

        logger.info("Scraping dynamic data...")
        data_dynamic = scrape_dynamic()

        # Combine
        all_data = data_static + data_dynamic
        logger.info(f"Total records scraped: {len(all_data)}")

        if not all_data:
            logger.warning("No data scraped. Exiting pipeline.")
            return

        # -------- CLEANING --------
        logger.info("Cleaning data...")
        df = clean_data(all_data)

        if df.empty:
            logger.warning("DataFrame is empty after cleaning.")
            return

        # -------- STORAGE --------
        logger.info("Saving to CSV...")
        save_to_csv(df, "data/processed/quotes.csv")

        logger.info("Saving to SQL...")
        save_to_sql(df)

        logger.info("✅ Pipeline completed successfully")

    except Exception as e:
        logger.exception(f"❌ Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()  