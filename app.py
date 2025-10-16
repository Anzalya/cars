import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("🚗  предсказание цены автомобиля (в сомах)")

data_path = "archive/CAR DETAILS FROM CAR DEKHO.csv"
df = pd.read_csv(data_path)

required_columns = ["name", "year", "selling_price", "km_driven", "fuel", "seller_type", "transmission", "owner"]
if not all(col in df.columns for col in required_columns):
    st.error("❌ В выбранном CSV-файле не хватает нужных столбцов.")
    st.stop()

df = df.dropna(subset=required_columns)
#строки с пропущенными значениями в нужных столбцах удаляются.
st.header("📋 Таблица с данными автомобилей")
st.dataframe(df.head(100))

exchange_rate = 1.1
df["selling_price"] = df["selling_price"] * exchange_rate

#создаем новые признаки 
df["car_age"] = 2025 - df["year"]
df["log_km_driven"] = np.log1p(df["km_driven"])

# Выберем новые признаки
features_cat = ["name", "fuel", "seller_type", "transmission", "owner"]
features_num = ["year", "car_age", "log_km_driven"]
target = "selling_price" 
#формируем x and y
X_cat = df[features_cat]
X_num = df[features_num]
y = df[target]
# преобразуются в one-hot encoding
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_cat_enc = encoder.fit_transform(X_cat)
#Объединяются категориальные и числовые признаки в
#  одну матрицу признаков X_final.

X_final = np.hstack([X_cat_enc, X_num.values])

X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.3, random_state=0
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred_test = model.predict(X_test)
errors = y_test - y_pred_test

mae = mean_absolute_error(y_test, y_pred_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2 = r2_score(y_test, y_pred_test)

st.subheader("📊 Метрики модели на тестовой выборке")
st.metric("R² (коэффициент детерминации)", f"{r2:.3f}")
st.metric("MAE (средняя абсолютная ошибка)", f"{mae:,.0f}")
st.metric("RMSE (корень из среднеквадратичной ошибки)", f"{rmse:,.0f}")


# Сортируем по фактической цене для "восходящего" графика
sort_idx = np.argsort(y_test)
y_test_sorted = y_test.iloc[sort_idx]
y_pred_sorted = y_pred_test[sort_idx]
errors_sorted = errors.iloc[sort_idx]

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.scatter(y_test_sorted, y_pred_sorted, alpha=0.5, color='blue')
    ax1.plot([y_test_sorted.min(), y_test_sorted.max()], [y_test_sorted.min(), y_test_sorted.max()], color='red', linewidth=3)
    ax1.set_xlabel("Фактическая цена (сом)", fontsize=14)
    ax1.set_ylabel("Предсказанная цена (сом)", fontsize=14)
    ax1.set_title("📈 Факт vs Предсказание (Тест)", fontsize=18)
    ax1.tick_params(axis='both', which='major', labelsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(9, 6))
    ax2.scatter(y_test_sorted, errors_sorted, alpha=0.5, color='purple')
    ax2.axhline(0, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel("Фактическая цена (сом)", fontsize=14)
    ax2.set_ylabel("Ошибка (Факт - Предсказание)", fontsize=14)
    ax2.set_title("📉 Ошибки предсказаний (Тест)", fontsize=18)
    ax2.tick_params(axis='both', which='major', labelsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# Ввод параметров автомобиля
st.header("🔧 Введите параметры автомобиля для прогноза")

name = st.selectbox("Марка/Модель автомобиля", sorted(df["name"].dropna().unique()))
year = st.slider("Год выпуска", int(df["year"].min()), int(df["year"].max()), 2015)
km_driven = st.slider("Пробег (в км)", 0, int(df["km_driven"].max()), 50000)
fuel = st.selectbox("Тип топлива", sorted(df["fuel"].dropna().unique()))
seller_type = st.selectbox("Тип продавца", sorted(df["seller_type"].dropna().unique()))
transmission = st.selectbox("Коробка передач", sorted(df["transmission"].dropna().unique()))
owner = st.selectbox("Тип владельца", sorted(df["owner"].dropna().unique()))
#Создание признаков из пользовательского ввода в нужном формате для модели.
input_cat = pd.DataFrame([{
    "name": name,
    "fuel": fuel,
    "seller_type": seller_type,
    "transmission": transmission,
    "owner": owner
}])

input_cat_enc = encoder.transform(input_cat)
input_num = np.array([[year, 2025 - year, np.log1p(km_driven)]])
input_final = np.hstack([input_cat_enc, input_num])

predicted_price = model.predict(input_final)[0]
st.subheader(f"💰 Предсказанная цена: **{predicted_price:,.0f} сом**")
 