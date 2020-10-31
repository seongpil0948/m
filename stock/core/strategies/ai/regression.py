import os
from tensorflow import keras
from django.conf import settings
from datetime import datetime

from stock.core.data.market import get_recently_price


__all__ = [
    'regression'
]

def regression(code='207940', end=None, start=None):
    # ascending models, sort by datetime
    model_path = os.path.join(settings.TRAINED_MODEL_DIR, 'regression')
    models = sorted(os.listdir(model_path))
    model = keras.models.load_model(os.path.join(
        model_path,
        models[-1]
    ))
    recent_date, close_price = get_recently_price(code)
    y_predicted = model.predict([close_price])

    return {
        'recent_date': y_predicted.flatten()[0]
    }
    
    
