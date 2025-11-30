import numpy as np

# Формула градиентного спуска
def update_weights(weights, gradients, learning_rate=0.01):
    """
    w_new = w_old - learning_rate * gradient
    """
    new_weights = []
    for w, grad in zip(weights, gradients):
        new_weights.append(w - learning_rate * grad)
    return new_weights

# Пример с одним весом
def simple_gradient_descent():
    # Минимизируем функцию f(w) = (w - 3)^2
    w = 0.0  # начальный вес
    learning_rate = 0.1
    epochs = 5
    
    print("Градиентный спуск для f(w) = (w - 3)^2")
    print(f"Начальный вес: {w}")
    
    for epoch in range(epochs):
        gradient = 2 * (w - 3)  # производная
        w = w - learning_rate * gradient  # обновление веса
        loss = (w - 3)**2
        print(f"Эпоха {epoch+1}: w = {w:.3f}, градиент = {gradient:.3f}, loss = {loss:.3f}")

# Пример с несколькими весами
def multi_weight_example():
    # Веса сети (2 слоя)
    weights = [
        np.array([[0.1, 0.2], [0.3, 0.4]]),  # слой 1
        np.array([[0.5], [0.6]])              # слой 2
    ]
    
    # Градиенты (рассчитанные через backpropagation)
    gradients = [
        np.array([[0.05, 0.1], [0.15, 0.2]]),  # градиенты слоя 1
        np.array([[0.25], [0.3]])               # градиенты слоя 2
    ]
    
    learning_rate = 0.1
    
    print("\nОбновление весов сети:")
    print("Старые веса:", [w.tolist() for w in weights])
    
    new_weights = update_weights(weights, gradients, learning_rate)
    
    print("Новые веса:", [w.tolist() for w in new_weights])


# Запуск демонстрации
if __name__ == "__main__":
    simple_gradient_descent()
    multi_weight_example()
