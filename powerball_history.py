import requests
import csv
from datetime import datetime
from datetime import date

class Draw:
    field_names = ['DrawDate', 'WB1', 'WB2', 'WB3', 'WB4', 'WB5', 'PB', 'PP']
    def __init__(self, input_line):
        #Parse line into the class
        self.draw_date = date.today()
        self.numbers = []
        self.powerball = -1
        self.powerplay = -1
        self.ConstructSelf(input_line)

    def Dict(self):
        return { 'DrawDate': self.draw_date.strftime("%d/%m/%Y"),
                 'WB1': self.numbers[0],
                 'WB2': self.numbers[1],
                 'WB3': self.numbers[2],
                 'WB4': self.numbers[3],
                 'WB5': self.numbers[4],
                 'PB': self.powerball,
                 'PP': self.powerplay
                 }

    def ConstructSelf(self, input_line):
        elements = input_line.split()
        self.ConstructDate(elements[0])
        self.ConstructNumbers(elements[1:])

    def ConstructDate(self, date_str):
        self.draw_date = datetime.strptime(date_str, "%m/%d/%Y")

    def ConstructNumbers(self, num_list):
        self.numbers = sorted(num_list[0:5])
        self.powerball = num_list[5]
        if len(num_list) == 7:
            self.powerplay = num_list[6]

def ParseContent(req, sort_asc=True):
    draws = []
    for line in req.text.splitlines()[1:]:
        draw = Draw(line)
        draws.append(draw)
    
    sorted_draws = sorted(draws, key=lambda draw: draw.draw_date, reverse=sort_asc)

    return sorted_draws

def WriteToCSV(draws):
    with open('powerball.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=Draw.field_names)
        writer.writeheader()
        for draw in draws:
            writer.writerow(draw.Dict())

print("Fetching numbers from Powerball.com")
r = requests.get('http://www.powerball.com/powerball/winnums-text.txt')
print("Parsing values")
draws = ParseContent(r, False)
print("Writing to CSV")
WriteToCSV(draws)
print("---DONE---")
