import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    import torch
    logger.debug("PyTorch imported successfully")
except ImportError as e:
    logger.error(f"Failed to import PyTorch: {e}")
    raise

try:
    import numpy as np
    logger.debug("NumPy imported successfully")
except ImportError as e:
    logger.error(f"Failed to import NumPy: {e}")
    raise

try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    logger.debug("Transformers imported successfully")
except ImportError as e:
    logger.error(f"Failed to import Transformers: {e}")
    raise

logger.debug(f"Python version: {sys.version}")
logger.debug(f"NumPy version: {np.__version__}")
logger.debug(f"PyTorch version: {torch.__version__}")

# Load FinBERT model and tokenizer
model_name = "ProsusAI/finbert"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()  # Set model to evaluation mode
    logger.debug("FinBERT model and tokenizer loaded successfully")
except Exception as e:
    logger.error(f"Error loading model or tokenizer: {e}")
    raise

def get_finbert_sentiment(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():  # Disable gradient calculation
            outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_scores = probabilities.detach().cpu().numpy()[0]
        sentiments = ["positive", "negative", "neutral"]
        sentiment = sentiments[np.argmax(sentiment_scores)]
        confidence = np.max(sentiment_scores)
        return sentiment, confidence
    except Exception as e:
        logger.error(f"Error in get_finbert_sentiment: {e}")
        return "neutral", 0.0  # Return a default value in case of error

def analyze_financial_text(text):
    try:
        sentiment, confidence = get_finbert_sentiment(text)
        return f"FinBERT Analysis: Sentiment: {sentiment}, Confidence: {confidence:.2f}"
    except Exception as e:
        logger.error(f"Error in analyze_financial_text: {e}")
        return "FinBERT Analysis: Unable to analyze text"