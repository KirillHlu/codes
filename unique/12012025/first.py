import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

# Пример данных: рост, вес, возраст
heights = np.array([150, 170, 160, 155, 180, 165])  # Рост в см
weights = np.array([45, 70, 60, 50, 80, 65])
ages = np.array([10, 15, 12, 11, 16, 14])

X = np.column_stack((heights, weights, ages))
y = np.array([0, 1, 0, 0, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer='l2'))
model.add(Dense(32, activation='relu', kernel_regularizer='l2'))
model.add(Dense(1, activation='sigmoid'))  # Для бинарной классификации

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=5)

model.fit(X_train, y_train, epochs=250, batch_size=8, validation_split=0.2, callbacks=[early_stopping])

# Оценка модели на тестовых данных
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}')
# Предположим, у нас есть новые данные для предсказания
new_data = np.array([[152, 50, 14],   # Пример 1: рост 160 см, вес 55 кг, возраст 12 лет
                     [180, 65, 14]])  # Пример 2: рост 175 см, вес 70 кг, возраст 15 лет

# Нормализация новых данных с использованием того же скейлера
new_data_scaled = scaler.transform(new_data)

# Использование модели для предсказания
predictions = model.predict(new_data_scaled)

# Преобразование предсказаний в бинарные метки (0 или 1)
predicted_classes = (predictions > 0.5).astype(int)

# Интерпретация результатов
for i, prediction in enumerate(predicted_classes):
    gender = "Мальчик" if prediction == 1 else "Девочка"
    print(f"Пример {i + 1}: {gender}")
