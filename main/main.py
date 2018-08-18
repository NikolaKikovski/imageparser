# Импортируем стандартные библиотеки
import os
import sys
from urllib import request
# Имортируем сторонние библиотеки
from PyQt5 import QtWidgets
from lxml import html
import requests
# Импортируем GUI шаблон
from untitled import Ui_MainWindow

# Main domain
url = 'https://www.smashingmagazine.com/'
# Месяца словами
month_names = ['january',
               'february',
               'march',
               'april',
               'may',
               'june',
               'july',
               'august',
               'september',
               'october',
               'november',
               'december']
# Месяца цифрами
month_int = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
# Отношение цифр к названиям
month_dict = dict(zip(month_int, month_names))


# Класс главного окна программы
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Connect UI (тут мне стало лень переключать раскладку)
        self.setupUi(self)
        # Connect button to function
        self.pushButton.clicked.connect(self.parse)

    # main parse/download function
    def parse(self):
        # get values from comboboxes
        month = self.comboBox.currentText()
        year = self.comboBox_2.currentText()
        resolution = self.comboBox_3.currentText()
        # format month and year for url
        if 1 < int(month) <= 10:
            my_month = '0'+str(int(month)-1)
            my_year = str(year)
        elif month == '01':
            my_month = '12'
            my_year = str(int(year) - 1)
        else:
            my_month = str(int(month)-1)
            my_year = str(year)
        print(my_month, my_year)
        # url with all images of selected month/year
        current_url = url+'%s/%s/desktop-wallpaper-calendars-%s-%s' % (my_year, my_month, month_dict[month], year)
        # get page
        response = requests.get(current_url)
        print(current_url)
        # parse body
        parsed_body = html.fromstring(response.text)
        # search all links
        links = parsed_body.xpath('//div[@class = "c-garfield-the-cat"]/ul/li/a')
        # iterate links
        for i in links:
            # search resolution in link
            if resolution in i.xpath('.//text()'):
                a = i.xpath('.//@href')[0]
                name_file = str(a).split('/')[-1]
                print('downloading....',name_file)
                save_dir = os.path.join('.\download', str(year), str(month), str(resolution))
                print('to directory....',save_dir)
                # noinspection PyBroadException
                try:
                    os.stat(save_dir)
                except:
                    os.makedirs(save_dir)
                request.urlretrieve(a, save_dir+'/'+name_file)
        print('\n\nSUCCESS !')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
