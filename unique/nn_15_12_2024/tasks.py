#1
import numpy as np


def sigmoid(x):
    # Функция активации sigmoid:: f(x) = 1 / (1 + e^(-x))
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # Производная от sigmoid: f'(x) = f(x) * (1 - f(x))
    fx = sigmoid(x)
    return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # y_true и y_pred являются массивами numpy с одинаковой длиной
    return ((y_true - y_pred) ** 2).mean()


class OurNeuralNetwork:
    """
    Нейронная сеть, у которой:
        - 2 входа
        - скрытый слой с двумя нейронами (h1, h2)
        - слой вывода с одним нейроном (o1)
    """

    def __init__(self):
        # Вес
        self.w1 = np.random.normal()
        self.w2 = np.random.normal()
        self.w3 = np.random.normal()
        self.w4 = np.random.normal()

        self.w5 = np.random.normal()
        self.w6 = np.random.normal()

        # Смещения
        self.b1 = np.random.normal()
        self.b2 = np.random.normal()
        self.b3 = np.random.normal()

    def feedforward(self, x):
        # x является массивом numpy с двумя элементами
        h1 = sigmoid(self.w1 * x[0] + self.w2 * x[1] + self.b1)
        h2 = sigmoid(self.w3 * x[0] + self.w4 * x[1] + self.b2)
        o1 = sigmoid(self.w5 * h1 + self.w6 * h2 + self.b3)
        return o1

    def train(self, data, all_y_trues):
        learn_rate = 0.1 # alpha, также называемый скоростью обучения
        epochs = 2000  # количество циклов во всём наборе данных

        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):

                # --- Выполняем обратную связь (нам понадобятся эти значения в дальнейшем)
                neuro_1_sum = self.w1 * x[0] + self.w2 * x[1] + self.b1
                neuro_1_result = sigmoid(neuro_1_sum)

                neuro_2_sum = self.w3 * x[0] + self.w4 * x[1] + self.b2
                neuro_2_result = sigmoid(neuro_2_sum)

                neuro_3_sum = self.w5 * neuro_1_result + self.w6 * neuro_2_result + self.b3
                neuro_3_result = sigmoid(neuro_3_sum)

                y_pred = neuro_3_result # текущее предсказание
                #d_L_d_ypred = deriv_sigmoid(y_pred) * (y_true - y_pred)
                # --- Подсчет частных производных
                # --- Наименование: d_L_d_w1 представляет "частично L / частично w1"
                d_L_d_ypred = -1 * (y_true - y_pred)

                # Нейрон o1
                d_ypred_d_w5 = neuro_1_result * deriv_sigmoid(neuro_3_sum) # изменение для веса 1 нейрона о1
                d_ypred_d_w6 = neuro_2_result * deriv_sigmoid(neuro_3_sum) # изменение для веса 2 нейрона о1
                d_ypred_d_b3 = deriv_sigmoid(neuro_3_sum)      # изменение для смещения нейрона о1

                d_ypred_d_h1 = self.w5 * deriv_sigmoid(neuro_3_sum)  # опускаемся в глубь к нейрону 1
                d_ypred_d_h2 = self.w6 * deriv_sigmoid(neuro_3_sum) # опускаемся в глубь к нейрону 2

                # Нейрон h1
                d_h1_d_w1 = x[0] * deriv_sigmoid(neuro_1_sum) # изменение для веса 2 нейрона h1
                d_h1_d_w2 = x[1] * deriv_sigmoid(neuro_1_sum) # изменение для веса 2 нейрона h1
                d_h1_d_b1 = deriv_sigmoid(neuro_1_sum) # изменение для смещения нейрона h1

                # Нейрон h2
                d_h2_d_w3 = x[0] * deriv_sigmoid(neuro_2_sum)
                d_h2_d_w4 = x[1] * deriv_sigmoid(neuro_2_sum)
                d_h2_d_b2 = deriv_sigmoid(neuro_2_sum)

                # --- Обновляем вес и смещения
                # Нейрон h1
                self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w1
                self.w2 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w2
                self.b1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1

                # Нейрон h2
                self.w3 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w3
                self.w4 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w4
                self.b2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_b2

                # Нейрон o1
                self.w5 -= learn_rate * d_L_d_ypred * d_ypred_d_w5
                self.w6 -= learn_rate * d_L_d_ypred * d_ypred_d_w6
                self.b3 -= learn_rate * d_L_d_ypred * d_ypred_d_b3

            # --- Подсчитываем общую потерю в конце каждой фазы
            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.feedforward, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f" % (epoch, loss))


#увлечения
data = np.array([
    [4, 5],  # Маша
    [1, 2],  # Петя
    [2, 3],  # Вася
    [5, 6],  # Оля
])

all_y_trues = np.array([
    1,  # Маша
    0,  # Петя
    0,  # Вася
    1,  # Оля
])

# Тренируем нашу нейронную сеть!
network = OurNeuralNetwork()
network.train(data, all_y_trues)

# Делаем предсказания
emily = np.array([4, 5])  #
frank = np.array([1, 3])  #

print(f"Emily:  {network.feedforward(emily):.3f}")  # 0.951 - F
print(f"Frank:  {network.feedforward(frank):.3f}")  # 0.039 - M


#2
import numpy as np


def sigmoid(x):
    # Функция активации sigmoid:: f(x) = 1 / (1 + e^(-x))
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # Производная от sigmoid: f'(x) = f(x) * (1 - f(x))
    fx = sigmoid(x)
    return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # y_true и y_pred являются массивами numpy с одинаковой длиной
    return ((y_true - y_pred) ** 2).mean()


class OurNeuralNetwork:
    """
    Нейронная сеть, у которой:
        - 2 входа
        - скрытый слой с двумя нейронами (h1, h2)
        - слой вывода с одним нейроном (o1)
    """

    def __init__(self):
        # Вес
        self.w1 = np.random.normal()
        self.w2 = np.random.normal()
        self.w3 = np.random.normal()
        self.w4 = np.random.normal()
        self.w5 = np.random.normal()
        self.w6 = np.random.normal()
        self.w7 = np.random.normal()
        self.w8 = np.random.normal()
        self.w9 = np.random.normal()

        self.w10 = np.random.normal()
        self.w11 = np.random.normal()
        self.w12 = np.random.normal()

        # Смещения
        self.b1 = np.random.normal()
        self.b2 = np.random.normal()
        self.b3 = np.random.normal()

        self.b4 = np.random.normal()

    def feedforward(self, x):
        # x является массивом numpy с двумя элементами
        h1 = sigmoid(self.w1 * x[0] + self.w4 * x[1] + self.w9 * x[2] + self.b1)
        h2 = sigmoid(self.w2 * x[0] + self.w5 * x[1] + self.w8 * x[2] + self.b2)
        h3 = sigmoid(self.w3 * x[0] + self.w6 * x[1] + self.w7 * x[2] + self.b3)
        o1 = sigmoid(self.w10 * h1 + self.w11 * h2 + self.w12 * h3 + self.b4)
        return o1

    def train(self, data, all_y_trues):
        learn_rate = 1 # alpha, также называемый скоростью обучения
        epochs = 20000  # количество циклов во всём наборе данных

        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):

                # --- Выполняем обратную связь (нам понадобятся эти значения в дальнейшем)
                neuro_1_sum = self.w1 * x[0] + self.w4 * x[1] + self.w9 * x[2] + self.b1
                neuro_1_result = sigmoid(neuro_1_sum)

                neuro_2_sum = self.w2 * x[0] + self.w5 * x[1] + self.w8 * x[2] + self.b2
                neuro_2_result = sigmoid(neuro_2_sum)

                neuro_3_sum = self.w3 * x[0] + self.w6 * x[1] + self.w7 * x[2] + self.b3
                neuro_3_result = sigmoid(neuro_3_sum)

                neuro_4_sum = self.w10 * neuro_1_result + self.w11 * neuro_2_result + self.w12 * neuro_3_result +self.b4
                neuro_4_result = sigmoid(neuro_4_sum)

                y_pred = neuro_4_result # текущее предсказание
                #d_L_d_ypred = deriv_sigmoid(y_pred) * (y_true - y_pred)
                # --- Подсчет частных производных
                # --- Наименование: d_L_d_w1 представляет "частично L / частично w1"
                d_L_d_ypred = -1 * (y_true - y_pred)

                # Нейрон o1
                d_ypred_d_w10 = neuro_1_result * deriv_sigmoid(neuro_4_sum) # изменение для веса 1 нейрона о1
                d_ypred_d_w11 = neuro_2_result * deriv_sigmoid(neuro_4_sum) # изменение для веса 2 нейрона о1
                d_ypred_d_w12 = neuro_3_result * deriv_sigmoid(neuro_4_sum)
                d_ypred_d_b4 = deriv_sigmoid(neuro_4_sum)      # изменение для смещения нейрона о1

                d_ypred_d_h1 = self.w10 * deriv_sigmoid(neuro_4_sum)  # опускаемся в глубь к нейрону 1
                d_ypred_d_h2 = self.w11 * deriv_sigmoid(neuro_4_sum) # опускаемся в глубь к нейрону 2
                d_ypred_d_h3 = self.w12 * deriv_sigmoid(neuro_4_sum)

                # Нейрон h1
                d_h1_d_w1 = x[0] * deriv_sigmoid(neuro_1_sum) # изменение для веса 2 нейрона h1
                d_h1_d_w4 = x[1] * deriv_sigmoid(neuro_1_sum) # изменение для веса 2 нейрона h1
                d_h1_d_w9 = x[2] * deriv_sigmoid(neuro_1_sum)
                d_h1_d_b1 = deriv_sigmoid(neuro_1_sum) # изменение для смещения нейрона h1

                # Нейрон h2
                d_h2_d_w2 = x[0] * deriv_sigmoid(neuro_2_sum)
                d_h2_d_w5 = x[1] * deriv_sigmoid(neuro_2_sum)
                d_h2_d_w8 = x[2] * deriv_sigmoid(neuro_2_sum)
                d_h2_d_b2 = deriv_sigmoid(neuro_2_sum)

                # Нейрон h3
                d_h3_d_w3 = x[0] * deriv_sigmoid(neuro_3_sum)
                d_h3_d_w6 = x[1] * deriv_sigmoid(neuro_3_sum)
                d_h3_d_w7 = x[2] * deriv_sigmoid(neuro_3_sum)
                d_h3_d_b3 = deriv_sigmoid(neuro_3_sum)

                # --- Обновляем вес и смещения
                # Нейрон h1
                self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w1
                self.w4 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w4
                self.w9 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w9
                self.b1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1

                # Нейрон h2
                self.w2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w2
                self.w5 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w5
                self.w8 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w8
                self.b2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_b2

                #нейрон h3
                self.w3 -= learn_rate * d_L_d_ypred * d_ypred_d_h3 * d_h3_d_w3
                self.w6 -= learn_rate * d_L_d_ypred * d_ypred_d_h3 * d_h3_d_w6
                self.w7 -= learn_rate * d_L_d_ypred * d_ypred_d_h3 * d_h3_d_w7
                self.b3 -= learn_rate * d_L_d_ypred * d_ypred_d_h3 * d_h3_d_b3

                # Нейрон o1
                self.w10 -= learn_rate * d_L_d_ypred * d_ypred_d_w10
                self.w11 -= learn_rate * d_L_d_ypred * d_ypred_d_w11
                self.w12 -= learn_rate * d_L_d_ypred * d_ypred_d_w12
                self.b4 -= learn_rate * d_L_d_ypred * d_ypred_d_b4

            # --- Подсчитываем общую потерю в конце каждой фазы
            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.feedforward, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f" % (epoch, loss))


#данные
data = np.array([
    [7, 0, 10],  # лимузин
    [3, 1, 50],  # кабриолет
    [8, 0, 0],  # лимузин
    [4, 1, 60],  # кабриолет
])

all_y_trues = np.array([
    0,  # лимузин
    1,  # кабриолет
    0,  # лимузин
    1,  # кабриолет
])

# Тренируем нашу нейронную сеть!
network = OurNeuralNetwork()
network.train(data, all_y_trues)

# Делаем предсказания
limousine = np.array([8, 0, 15])  #
convertible_car = np.array([4, 1, 60])  #

print(f"First car:  {network.feedforward(limousine):.3f}")  # 0.951 - F
print(f"Second car:  {network.feedforward(convertible_car):.3f}")  # 0.039 - M

