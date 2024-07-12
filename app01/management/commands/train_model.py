# ��app�´���һ��management/commandsĿ¼��Ȼ�󴴽�һ��train_model.py�ļ�
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from django.core.management.base import BaseCommand
from app01.models import VisitorPrediction
import pickle


class Command(BaseCommand):
    help = 'Train the visitor prediction model'

    def handle(self, *args, **kwargs):
        data = VisitorPrediction.objects.all().values()
        df = pd.DataFrame(data)

        X = df[['date_type', 'weather_condition', 'temperature', 'promotion']]
        y = df['visitors']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        with open('visitor_model.pkl', 'wb') as file:
            pickle.dump(model, file)

        self.stdout.write(self.style.SUCCESS('Model trained and saved successfully'))
