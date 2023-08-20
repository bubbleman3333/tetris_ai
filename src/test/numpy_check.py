import time

from sklearn.neural_network import MLPRegressor
import numpy as np

# 10個のデータポイントを生成
num_samples = 10
num_features = 100

# ランダムな特徴量を持つデータを生成
X = np.random.rand(num_samples, num_features)

# 各データポイントに対する目標値を設定（1から10までのランダムな値）
y = np.random.randint(1, num_features, size=num_samples)

# MLPRegressorモデルの定義（隠れ層1層、ユニット数10）
model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

start = time.time()
# モデルのトレーニング
model.fit(X, y)
print(time.time()-start)
# トレーニング後のモデルを使用して予測を行う
start = time.time()
predictions = model.predict(X)
print(y)
# 予測結果を表示
print("予測結果:", predictions)

print(time.time()-start)