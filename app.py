from flask import Flask, request, render_template,send_file,redirect,url_for,flash, send_from_directory
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from flask_caching import Cache
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager,login_user,logout_user,login_required
import json
import os

#Models
import models.dataconsult as dataconsult


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 86400}) # 1 day in seconds

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image1.png')
# @cache.cached()
def image():
    # # Create a new buffer and write the PNG image data to it
    plt.clf()
    png_output = BytesIO()
    df = dataconsult.plotData()

    descompositionResults = seasonal_decompose(df["Valor"],
                                            model = "additive")
    (descompositionResults
    .plot()
    .suptitle("Descomposicion Aditiva IMAE"))
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    canvas = FigureCanvas(fig)
    canvas.print_png(png_output)

    # Return the PNG image from the new buffer
    png_output.seek(0)
    return send_file(png_output, mimetype='image/png')

@app.route('/plot2.png')
# @cache.cached()
def image2():
    # # Create a new buffer and write the PNG image data to it
    plt.clf()
    png_output = BytesIO()
    df = dataconsult.plotData()

    WINDOW_SIZE =12
    df["rolling_mean"] = df["Valor"].rolling(window=WINDOW_SIZE).mean()
    df["rollingstd"] = df["Valor"].rolling(window=WINDOW_SIZE).std()
    df.plot(title="IMAE")
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    canvas = FigureCanvas(fig)
    canvas.print_png(png_output)
    image_data = png_output.getvalue()

    # Generate a URL for the image
    url = '/plot2.png?' + str(hash(image_data))

    cache.set(url, image_data)

    return redirect(url)

# def status401(error):
#     return redirect(url_for('index'))

if __name__=="__main__":
    # app.register_error_handler(401,status401)
    app.run(debug=True)