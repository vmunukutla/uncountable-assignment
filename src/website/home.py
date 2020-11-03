from flask import Flask, render_template, request
import psycopg2
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)

def formulateScatterQuery(input, output):
    input = input.replace(' ', '_').replace('-', '_')
    output = output.replace(' ', '_').replace('-', '_')
    query = 'SELECT inputs.{}, outputs.{} FROM inputs, outputs WHERE inputs.experiment = outputs.experiment;'
    query = query.format(input, output)
    return query

def createPlot(data, input, output):
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    x = np.zeros(len(data))
    y = np.zeros(len(data))
    for i in range(len(data)):
        x[i] = data[i][0]
        y[i] = data[i][1]
    ax.scatter(x, y)
    ax.set_xlabel(input)
    ax.set_ylabel(output)
    ax.set_title(f'Scatter plot for lab data')
    ax.grid(True)

    img = io.StringIO()
    fig.savefig(img, format='svg')
    svg_img = '<svg' + img.getvalue().split('<svg')[1]

    return svg_img

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scatter", methods=['GET', 'POST'])
def scatter():
    if request.method == 'POST':
        cur = None
        conn = None
        try:
            conn = psycopg2.connect("host=localhost dbname=uncountable user=vikas")
            cur = conn.cursor()
            input = request.form.get('input')
            output = request.form.get('output')
            query = formulateScatterQuery(input, output)
            cur.execute(query)
            data1 = cur.fetchall()
            plot = createPlot(data1, input, output)
        except Exception as e:
            pass
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

        return render_template("scatter.html", plot=plot)

    return render_template("scatter.html")


if __name__ == "__main__":
    app.run()
