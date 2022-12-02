from sklearn.preprocessing import OneHotEncoder

def encode_day_month(X):
    encoder = OneHotEncoder()
    X_proc = encoder.fit_transform(X)
    return X_proc
