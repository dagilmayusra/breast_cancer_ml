from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

# flask tanımlandı
app = Flask(__name__)
# eğitilen dosyanın yüklenmesi
model = pickle.load(open('model.pkl', 'rb'))


# Bu bizi ana index.html dosyasına yönlendirecektir.
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    # Birden çok girişi numpy dizisine dönüştürme
    int_features = [int(x) for x in request.form.values()]

    # Veri kümesindeki tümör sütunları
    features_name = ['Clump Thickness','Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion',
    'Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses']

    # Giriş değerlerini tahmin etme
    d ={j: int_features[i] for i, j in enumerate(features_name)}
    df = pd.DataFrame(d, index=[0])
    output = model.predict(df)
    d["Class"] = output[0]
    predict_df = pd.read_csv("static/predict.csv")
    print(predict_df)
    predict_df = predict_df.append(d, ignore_index= True)
    predict_df.to_csv("static/predict.csv", index=False)

    if output == 4:
        output = "Hasta Göğüs Kanseri"
    else:
        output = "Hasta Göğüs Kanseri Değil."

    return render_template('index.html', prediction=f'{output}', d='Download')

# uygulamayı localhost da çalıştırma
if __name__ == "__main__":
    app.run(debug=True)