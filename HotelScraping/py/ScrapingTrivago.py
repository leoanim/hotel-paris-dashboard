#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import commonFunctions as cf
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class ScrapingTrivago:

    def __init__(self, filename, city, start_date,
                 end_date, nbr_adults, children_age_array, nbr_room):
        self.__filename = filename
        self.__city = city
        self.__start_date = start_date
        self.__end_date = end_date
        self.__nbr_adults = nbr_adults
        self.__children_age_array = children_age_array
        self.__nbr_children = len(children_age_array)
        self.__nbr_room = nbr_room
        self.__csv_file_name_path()
        self.__driver = None

    def __csv_file_name_path(self):
        self.__filename = "../csv/trivago/{}_{}_to_{}_{}_adults_{}_children_{}_rooms.csv". \
            format(self.__filename, self.__start_date,
                   self.__end_date, self.__nbr_adults,
                   self.__nbr_children, self.__nbr_room)

    def process_search_results(self):
        self.__driver = webdriver.Firefox()
        self.__driver.maximize_window()
        self.__driver.get("https://www.trivago.fr")
        self.__click_cookies_button()
        self.__select_hotel_tab()
        self.__write_city()
        self.__select_date(self.__start_date)
        self.__select_date(self.__end_date)
        self.__select_guests()
        self.__validate_research()
        time.sleep(40)
        self.__driver.find_element(by="xpath", value="//body").send_keys(Keys.CONTROL + 'r')
        time.sleep(10)
        self.__click_maps_and_filter_buttons()

    def copy_hotels(self):
        self.__copy_hotels_to_csv_loop()
        self.__driver.close()
        # self.__driver = None

    def force_driver_close(self):
        self.__driver.close()

    def __click_cookies_button(self):
        time.sleep(2)
        wait = WebDriverWait(self.__driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        element = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        element.click()

    def __select_hotel_tab(self):
        time.sleep(2)
        self.__driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()

    def __write_city(self):
        time.sleep(2)
        self.__driver.find_element(by="id", value="input-auto-complete").send_keys(self.__city)
        time.sleep(2)
        self.__driver.find_element(by="id", value="react-autowhatever-1--item-0").click()

    def __select_date(self, date_chosen):
        time.sleep(2)
        date_chosen = cf.date_format_us_to_website(date_chosen)
        try:
            self.__driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
                .find_element(by="xpath", value="..") \
                .click()
        except:
            date_chosen_arr = date_chosen.split('-')
            date_calendar = self.__driver.find_element(by="xpath",
                                                       value="//button[contains(@class, 'cursor-auto font-bold')]") \
                .text.split(' ')
            while date_calendar[1] != date_chosen_arr[1] and date_calendar[1] != date_chosen_arr[1]:
                time.sleep(2)
                self.__driver.find_element(by="xpath", value="//button[@data-testid='calendar-button-next']").click()
                date_calendar = self.__driver.find_element(by="xpath",
                                                           value="//button[contains(@class, 'cursor-auto font-bold')]") \
                    .text.split(' ')
                date_calendar = [date_calendar[1], cf.month_digits_dictionary[date_calendar[0]]]

            time.sleep(2)
            self.__driver.find_element(by="xpath", value="//time[@datetime='" + date_chosen + "']") \
                .find_element(by="xpath", value="..") \
                .click()

    def __select_guests(self):
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-12").click()
        self.__driver.find_element(by="id", value="number-input-12").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-12").send_keys(self.__nbr_adults)
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-13").click()
        self.__driver.find_element(by="id", value="number-input-13").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-13").send_keys(self.__nbr_children)
        time.sleep(2)
        self.__driver.find_element(by="id", value="number-input-14").click()
        self.__driver.find_element(by="id", value="number-input-14").send_keys(Keys.CONTROL + 'a')
        self.__driver.find_element(by="id", value="number-input-14").send_keys(self.__nbr_room)
        time.sleep(2)
        if self.__nbr_children > 0:
            self.__select_children_ages()
        self.__driver.find_element(by="xpath", value="//button[@data-testid='guest-selector-apply']").click()

    def __select_children_ages(self):
        time.sleep(2)
        children_ages_select = self.__driver.find_element(by="xpath", value="//fieldset[@id='childAgeSelector']")
        children_ages_select = children_ages_select.find_elements(by="xpath", value="./ul/li/select")
        for child, age in zip(children_ages_select, self.__children_age_array):
            time.sleep(1)
            child.click()
            time.sleep(1)
            child.find_element(by="xpath", value="./option[@value='" + str(age) + "']").click()

    def __validate_research(self):
        self.__driver.find_element(by="xpath", value="//button[@data-testid='search-button']").click()
        time.sleep(2)

    def __click_maps_and_filter_buttons(self):
        time.sleep(4)
        self.__driver.find_element(by="xpath", value="//label[@data-title='Hôtel']").click()  # Click hotel view filter
        time.sleep(2)
        self.__driver.find_element(by="xpath",
                                   value="//button[@data-testid='switch-view-button-desktop']").click()  # Click map cross
        time.sleep(2)

    def __copy_hotels_to_csv_loop(self):
        # self.__click_maps_and_filter_buttons()
        next_page_button_present = True
        while next_page_button_present:
            self.__scroll_page()
            self.__get_hotels()
            try:
                self.__driver.find_element(by="xpath", value="//button[@data-testid='next-result-page']").click()
            except:
                next_page_button_present = False

    def __get_hotels(self):
        try:
            self.__click_all_localisation_buttons()
            time.sleep(4)
            locations_list = self.__get_hotels_location()

            names = self.__get_hotels_name()
            stars = self.__get_hotels_stars()
            prices = self.__get_hotels_price()
            grades = self.__get_hotels_grade()
            gps = self.__get_hotels_gps(locations_list)
            start_date = self.__start_date
            end_date = self.__end_date
            links = self.__get_hotels_link()

            cf.addRows(
                names=names,
                stars=stars,
                prices=prices,
                grades=grades,
                gps=gps,
                addresses=locations_list,
                start_date=start_date,
                end_date=end_date,
                links=links,
                filename=self.__filename,
                is_head=int(self.__get_current_page()) == 1,
                nb_adults=[self.__nbr_adults for _ in range(len(names))],
                nb_children=[self.__nbr_children for _ in range(len(names))],
                nb_room=[self.__nbr_room for _ in range(len(names))],
            )
            print("SUCCESS in copying data from one page.")
        except:
            print("ERROR page can't be saved into csv file.")
            # self.__driver.refresh()
            # self.__get_hotels()

    def __click_all_localisation_buttons(self):
        time.sleep(2)
        addresses_buttons = self.__driver.find_elements(by="xpath",
                                                        value="//button[@data-testid='distance-label-section']")
        time.sleep(2)
        for addressButton in addresses_buttons:
            time.sleep(0.5)
            self.__scroll_page()
            # wait = WebDriverWait(self.__driver, 10)
            # element = wait.until(EC.presence_of_element_located(addressButton))
            # element = wait.until(EC.element_to_be_clickable(element))
            # element.click()
            addressButton.click()
        show_hotels_policies_buttons = self.__driver \
            .find_elements(by="xpath", value="//button[@data-testid='hotel-policies-show-more']")
        for showHotelPoliciesButton in show_hotels_policies_buttons:
            time.sleep(0.5)
            showHotelPoliciesButton.click()

    def __scroll_page(self):
        # self.__driver.find_element(by="css selector", value="body").send_keys(Keys.CONTROL, Keys.END)
        self.__driver.find_element(by="css selector", value="body").send_keys(Keys.CONTROL, Keys.ARROW_DOWN)
        time.sleep(2)

    def __get_hotels_name(self):
        return list(
            map(lambda name: name.text,
                self.__driver.find_elements(by="xpath", value="//button[@data-testid='item-name']")))

    def __get_hotels_grade(self):
        return list(
            map(lambda grade: grade.text,
                self.__driver.find_elements(by="xpath", value="//span[@itemprop='ratingValue']")))

    def __get_hotels_price(self):
        return list(
            map(lambda price: price.text.replace("€", ""),
                self.__driver.find_elements(by="xpath", value="//p[@itemprop='price']")))

    def __get_hotels_location(self):
        return list(
            map(lambda location: location.text,
                self.__driver.find_elements(by="xpath", value="//address[@data-testid='info-slideout-map-address']")))

    def __get_hotels_gps(self, locations_list):
        return list(
            map(lambda location: cf.getLocalisationFromAdd(location), locations_list))

    def __get_hotels_link(self):
        return list(
            map(lambda link: link.get_attribute("href"),
                self.__driver.find_elements(by="xpath", value="//a[@itemprop='url']")))

    def __get_hotels_stars(self):
        accommodation_type_list = self.__driver.find_elements(by="xpath",
                                                              value="//button[@data-testid='accommodation-type']")
        stars_hotels_list = []
        for accommodation_type in accommodation_type_list:
            try:
                stars_hotels_list \
                    .append(
                    accommodation_type.find_element(by="xpath", value="./span/span/meta[@itemprop='ratingValue']") \
                        .get_attribute("content"))
            except:
                stars_hotels_list.append(np.nan)
        return stars_hotels_list

    def __get_current_page(self):
        try:
            return self.__driver.find_element(by="xpath", value="//button[@aria-current='page']").text
        except:
            return "1"


if __name__ == '__main__':
    # MM/DD/YYYY
    booking_trivago = ScrapingTrivago("trivago", "Paris", '05-11-2022', '05-12-2022', 1, [], 2)
    booking_trivago.process_search_results()
    booking_trivago.copy_hotels()
