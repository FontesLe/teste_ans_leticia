import logging
from typing import Optional
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ans_tests.log'),
            logging.StreamHandler()
        ]
    )

def format_currency(value: float) -> str:
    return f"R${value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def parse_date(date_str: str, formats: list = None) -> Optional[datetime]:
    if formats is None:
        formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None