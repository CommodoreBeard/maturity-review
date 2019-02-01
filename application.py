import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from forms import CsvForm
from csv_parser import parse, remove_nulls, gen_weighted_score, \
    gen_max_weighted_score, gen_total_max_weighted_score_per_topic, gen_maturity, gen_avg_maturity
from write_csv import write

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CsvForm()
    if form.validate_on_submit():
        f = form.csv.data
        filename = "raw_input.csv"
        f.save(os.path.join(
            app.instance_path, 'uploads', filename
        ))

        parsed = parse(os.path.join(
            app.instance_path, 'uploads', filename
        ))
        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        parsed = gen_avg_maturity(parsed)
        write(parsed, os.path.join(
            app.instance_path, 'processed', "processed.csv"))

        return send_from_directory(directory=os.path.join(
            app.instance_path, 'processed'), filename="processed.csv")

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)