import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


def train_stock_price_prediction_models(df, prediction_file_path):
    features = ["volume", "200dma", "RSI", "stochastic_oscillator", "ROC"]
    target = "next_day_close"
    df[target] = df.groupby("name")["close"].shift(-1)

    df.dropna(inplace=True)

    train_df, val_df, test_df = split_by_ticker(df, target)

    X_train, y_train = train_df[features], train_df["next_day_close"]
    X_val, y_val = val_df[features], val_df["next_day_close"]
    X_test, y_test = test_df[features], test_df["next_day_close"]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    lr_model = Lasso(alpha=3)
    lr_model.fit(X_train_scaled, y_train)
    lr_preds = lr_model.predict(X_val_scaled)

    xgb_model = XGBRegressor(n_estimators=100, learning_rate=1.5, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_val)

    lr_mae, lr_rmse, lr_r2, lr_mape = evaluate_model("Lasso Regression", y_val, lr_preds)
    xgb_mae, xgb_rmse, xgb_r2, xgb_mape = evaluate_model("Gradient Boosting (XGBoost)", y_val, xgb_preds)

    if lr_r2 > xgb_r2:
        lr_test_preds = lr_model.predict(X_test_scaled)
        test_df["predicted_price"] = lr_test_preds
        test_df.to_csv(prediction_file_path, index=False)
    else:
        xgb_test_preds = xgb_model.predict(X_test)
        test_df["predicted_price"] = xgb_test_preds
        test_df.to_csv(prediction_file_path, index=False)


def split_by_ticker(df, target, test_size=0.2):
    train_list = []
    test_list = []
    val_list = []

    for ticker, ticker_df in df.groupby("name"):
        ticker_df = ticker_df.sort_values("date")
        X = ticker_df.loc[:, df.columns != target]
        y = ticker_df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=1)

        train_list.append(pd.concat([X_train, y_train], axis=1))
        test_list.append(pd.concat([X_test, y_test], axis=1))
        val_list.append(pd.concat([X_val, y_val], axis=1))

    train_df = pd.concat(train_list).reset_index(drop=True)
    test_df = pd.concat(test_list).reset_index(drop=True)
    val_df = pd.concat(val_list).reset_index(drop=True)

    return train_df, val_df, test_df


def evaluate_model(model_name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    print(f"{model_name} - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}, MAPE: {mape:.4f}")
    return mae, rmse, r2, mape
