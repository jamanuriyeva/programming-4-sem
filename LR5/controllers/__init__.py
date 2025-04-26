# class ViewController():
#
#     def __init__(self, currency_rates):
#         import jinja2
#         from jinja2 import Environment,  FileSystemLoader
#         import os
#
#         self.values = currency_rates.values
#
#         self.currency_name = currency_rates.values[0]
#         self.currency_date = currency_rates.values[1]
#         self.currency_value = currency_rates.values[2]
#
#         self.environment = jinja2.Environment(loader=FileSystemLoader(os.getcwd()))
#
#     def __call__(self):
#         return f"{self.currency_name} - {self.currency_date} - {self.currency_value}"
#
#     def jinja2_view(self):
#
#         import time
#         current_time = time.time()
#         time_string = time.ctime(current_time)
#
#         self.template = self.environment.get_template("index.html")
#         result_html = self.template.render( valutes = self.values)
#
#         return result_html

from jinja2 import Environment, FileSystemLoader
import os


class ViewController:
    def __init__(self, values):
        self.values = values
        self.environment = Environment(
            loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')))

    def __call__(self):
        if len(self.values) >= 3:
            return f"{self.values[0]} - {self.values[1]} - {self.values[2]}"
        return "No data available"

    def jinja2_view(self):
        template = self.environment.get_template("index.html")
        return template.render(valutes=self.values)