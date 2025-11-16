#!/usr/bin/env python3
"""
turnover_prediction.py
Employee Turnover Prediction Model
Author: Deepanraj A
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_hr_data(filepath='data/employee_data.csv'):
    """Load employee data for turnover analysis"""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} employee records")
    return df

def engineer_features(df):
    """Create features for turnover prediction"""
    # Tenure bins
    df['tenure_years'] = df['tenure_months'] / 12
    df['tenure_category'] = pd.cut(df['tenure_years'], 
                                   bins=[0, 1, 3, 5, 10, 50],
                                   labels=['<1yr', '1-3yr', '3-5yr', '5-10yr', '10+yr'])
    
    # Performance indicators
    df['performance_score'] = (df['last_review_score'] + df['avg_project_rating']) / 2
    df['high_performer'] = (df['performance_score'] > 4.0).astype(int)
    
    # Work-life balance
    df['overworked'] = (df['avg_hours_per_week'] > 50).astype(int)
    df['promotion_due'] = (df['years_since_promotion'] > 3).astype(int)
    
    return df

def train_turnover_model(X_train, y_train, model_type='rf'):
    """Train employee turnover prediction model"""
    if model_type == 'rf':
        model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    else:
        model = GradientBoostingClassifier(n_estimators=150, random_state=42)
    
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate turnover prediction model"""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return accuracy, roc_auc

def main():
    # Load data
    df = load_hr_data()
    
    # Feature engineering
    df = engineer_features(df)
    
    # Prepare features
    feature_cols = ['age', 'tenure_months', 'department_encoded', 'salary',
                    'satisfaction_score', 'last_review_score', 'projects_count',
                    'avg_hours_per_week', 'promotion_due', 'overworked']
    
    X = df[feature_cols]
    y = df['left']  # Target: 1 if employee left, 0 otherwise
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    print("Training turnover prediction model...")
    model = train_turnover_model(X_train, y_train, model_type='rf')
    
    # Evaluate
    evaluate_model(model, X_test, y_test)
    
    # Feature importance
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop Features Predicting Turnover:")
    print(importance.head(10))
    
    # Save model
    joblib.dump(model, 'models/turnover_model.pkl')
    print("\nModel saved to models/turnover_model.pkl")

if __name__ == '__main__':
    main()
