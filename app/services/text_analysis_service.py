from collections import Counter
import re
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session

from app.models.part import Part


class TextAnalysisService:
    @staticmethod
    def get_common_words(db: Session, limit: int = 5) -> List[Dict[str, any]]:
        parts = db.query(Part).filter(Part.description.is_not(None)).all()

        descriptions = [part.description for part in parts if part.description]

        if not descriptions:
            return []

        all_text = " ".join(descriptions).lower()

        cleaned_text = re.sub(r'[^\w\s]', ' ', all_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # Split text into words
        words = cleaned_text.split()

        # Filter out common stop words (optional)
        # stop_words = {
        #     'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'for', 'to',
        #     'in', 'of', 'with', 'by', 'at', 'from', 'on', 'used'
        # }

        stop_words = {}

        filtered_words = [word for word in words if word not in stop_words]

        # Count word frequencies
        word_counts = Counter(filtered_words)

        # Get most common words
        most_common = word_counts.most_common(limit)

        # Format result
        result = [{"word": word, "count": count} for word, count in most_common]

        return result
