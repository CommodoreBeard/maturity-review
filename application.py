import os

from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap

from forms import CsvForm
from data_handler import DataHandler
from write_csv import write_full_data

application = Flask(__name__)
application.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def index():
    form = CsvForm()
    if form.validate_on_submit():
        file = form.csv.data
        filename = "raw_input.csv"
        file_path = os.path.join(application.instance_path, 'uploads', filename)
        file.save(file_path)

        data_handler = DataHandler(file_path)
        processed = data_handler.process_data()
        data_for_chart = data_handler.format_for_chart(processed)

        write_full_data(processed, os.path.join(
            application.instance_path, 'processed', "processed.csv"))

        write_full_data(data_for_chart, os.path.join(
            application.instance_path, 'processed', "data_for_chart.csv"))

        labels = list(data_for_chart[0].keys())
        values = list(data_for_chart[0].values())
        return render_template(
            'chart.html',
            title="Maturity Review",
            max=100,
            labels=labels,
            values=values)

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
    application.run("0.0.0.0", port=80)
