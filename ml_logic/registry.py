import mlflow
from mlflow.tracking import MlflowClient
import glob
import os
from colorama import Fore, Style
from tensorflow.keras import Model, models
import pandas as pd


def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    #timestamp = time.strftime("%Y%m%d-%H%M%S")

    #print(Fore.BLUE + "\nSave model to local disk..." + Style.RESET_ALL)

    # save params
    if params is not None:
        params_path = os.path.join(LOCAL_REGISTRY_PATH, "params", X_train_station + ".pickle")
        print(f"- params path: {params_path}")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics
    if metrics is not None:
        metrics_path = os.path.join(LOCAL_REGISTRY_PATH, "metrics", X_train_station + ".pickle")
        print(f"- metrics path: {metrics_path}")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # save model
    if model is not None:
        model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", X_train_station)
        print(f"- model path: {model_path}")
        model.save(model_path)

    print("\n✅ data saved locally")

    return None


def load_model(X_new) -> Model:
    """
    load the latest saved model, return None if no model found
    """

    station_list = []
    pred_list = []
    # get latest model version
    model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")

    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    for model_path in results:
        print(f"- path: {model_path}")
        station_name = model_path[-3:]
        station_list.append(station_name)
        model = models.load_model(model_path)
        pred_list.append(round(model.predict(X_new)[0][0],0))

    pred_df = pd.DataFrame(zip(station_list, pred_list))

    return pred_df
