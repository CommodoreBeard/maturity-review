import os

from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from forms import CsvForm
from csv_parser import parse, remove_nulls, gen_weighted_score, \
    gen_max_weighted_score, gen_total_max_weighted_score_per_topic, gen_maturity, gen_avg_maturity, format_for_chart
from write_csv import write_full_data

application = Flask(__name__)
application.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def index():
    form = CsvForm()
    if form.validate_on_submit():
        f = form.csv.data
        filename = "raw_input.csv"
        f.save(os.path.join(
            application.instance_path, 'uploads', filename
        ))

        parsed = parse(os.path.join(
            application.instance_path, 'uploads', filename
        ))

        parsed = remove_nulls(parsed)
        parsed = gen_weighted_score(parsed)
        parsed = gen_max_weighted_score(parsed)
        parsed = gen_total_max_weighted_score_per_topic(parsed)
        parsed = gen_maturity(parsed)
        parsed = gen_avg_maturity(parsed)
        data_for_chart = format_for_chart(parsed)

        write_full_data(parsed, os.path.join(
            application.instance_path, 'processed', "processed.csv"))
        
        write_full_data(data_for_chart, os.path.join(
            application.instance_path, 'processed', "data_for_chart.csv"))

        labels = list(data_for_chart[0].keys())
        values = list(data_for_chart[0].values())
        return render_template('chart.html', title="Maturity Review", max=100, labels=labels, values=values)

    return render_template('index.html', form=form)

@application.route('/download_raw')
def download_processed_csv():
    return send_file(os.path.join(application.instance_path, 'processed', 'processed.csv'),
                     mimetype='text/csv',
                     attachment_filename='processed.csv',
                     as_attachment=True)

@application.route('/download_chart')
def download_chart_csv():
    return send_file(os.path.join(application.instance_path, 'processed', 'data_for_chart.csv'),
                     mimetype='text/csv',
                     attachment_filename='data_for_chart.csv',
                     as_attachment=True)

if __name__ == '__main__':
    application.debug = True
    application.run()