import numpy as np
import time


class Fuzzy:
    def __init__(self):
        self.temp = 0  # temperature
        self.cld = 0  # cloudiness
        self.t_crt = 0  # current time
        self.led_out = 0  # led output
        self.t_sunrise = 0
        self.t_sunset = 0

    def update_data(self, new_temp=None, new_cld=None, new_time=None):
        if new_temp:
            self.temp = new_temp
        if new_cld:
            self.cld = new_cld
        if new_time:
            self.t_crt = new_time

    def update_sun(self, tr, ts):
        self.t_sunrise = tr
        self.t_sunset = ts

    def temp_prob(self):
        temp = self.temp
        cold = float(np.piecewise(temp, [temp < 60, (temp >= 60) and (temp < 70), temp >= 70], [1, 7-0.1*temp, 0]))
        warm = float(np.piecewise(temp, [temp < 75, temp > 75], [0.1*temp - 6.5, 7.5-0.1*temp]))
        warm = max(warm, 0)  # make sure value is positive
        hot = float(np.piecewise(temp, [temp < 90, temp >= 90], [0.1*temp-8, 1]))
        hot = max(hot, 0)

        prob_arr = [cold, warm, hot]
        # print("temp", prob_arr)
        return prob_arr

    def cld_prob(self):
        cld_lv = self.cld
        # distribution for different cloudiness states
        sunny = float(np.piecewise(cld_lv, [cld_lv < 25, cld_lv >= 25], [1, 2.6667-0.0666 * cld_lv]))
        sunny = max(sunny, 0)
        scld = float(np.piecewise(cld_lv, [cld_lv < 50, cld_lv >= 50], [0.0666*cld_lv - 2.3334, 4.3333-0.0666*cld_lv]))
        scld = max(scld, 0)
        cld = float(np.piecewise(cld_lv, [cld_lv < 75, cld_lv >= 75], [0.0666*cld_lv - 4, 1]))
        cld = max(cld, 0)

        prob_arr = [sunny, scld, cld]
        # print("cld", prob_arr)
        return prob_arr

    def time_prob(self):
        dt_crt = min(self.t_crt-self.t_sunrise, self.t_sunset-self.t_crt)
        dt_crt = max(dt_crt, 0)  # negative to zero
        del_t = self.t_sunset - self.t_sunrise
        t_prop = dt_crt/del_t
        night = max(1-6.666*t_prop, 0)
        # sunrise/sunset
        srss = float(np.piecewise(t_prop, [t_prop < 0.2, t_prop >= 0.2], [10*t_prop - 1, 3 - 10*t_prop]))
        srss = max(srss, 0)
        day = float(np.piecewise(t_prop, [t_prop < 0.25, t_prop >= 0.25], [10*t_prop-1.5, 1]))
        day = max(day, 0)

        prob_arr = [day, srss, night]
        # print("time", prob_arr)
        return prob_arr

    def de_fuzz(self):
        # update mu's
        mu1 = max(self.time_prob()[2], self.cld_prob()[2])
        mu2 = min(self.time_prob()[1], max(self.temp_prob()[0], self.cld_prob()[1]))
        mu3 = min(self.time_prob()[1], max(self.temp_prob()[0], self.cld_prob()[0]))
        mu4 = min(self.time_prob()[0], max(self.temp_prob()[2], self.cld_prob()[1]))
        mu5 = min(self.time_prob()[0], self.cld_prob()[0])
        mu = [mu5, mu4, mu3, mu2, mu1]
        mu_sum = sum(mu)
        mu = np.array(mu)
        print(mu)
        weight = np.array([0, 0.25, 0.5, 0.75, 1]).T

        # calc centroid
        mu_sum_weight = np.matmul(mu, weight)
        self.led_out = mu_sum_weight/mu_sum


def main():
    fuz = Fuzzy()
    fuz.update_sun(7, 17)
    fuz.update_data(76.0, 44.0, 14.8)
    fuz.de_fuzz()
    print(fuz.led_out)


main()



