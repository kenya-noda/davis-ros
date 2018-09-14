#! /usr/bin/env python3

from weather import units
import weather.stations.davis_weatherLinkIP as weatherlink
import rospy
import time
import davis.msg


class Davis(object):

    def __init__(self, ip, port=22222):
        node_name = "davis"
        rospy.init_node(node_name)
        self.ip = ip
        self.port = port

    def pub_func(self):
        """
        Publish Function
        parse() function returns dictionary "fields"
        "fields" has some weather data, and sends "b'\n\r'" as EOL
        check EOL, and publish the weather data to ROS_weather.py
        """
        pub = rospy.Publisher("davis_weather", davis.msg.davis_weather, queue_size = 1)
        msg = davis.msg.davis_weather()
        while not rospy.is_shutdown():
            # connect to Vantage Pro 2
            vantage = weatherlink.VantagePro(self.ip, self.port)
            ret = vantage.parse()
            if ret["EOL"] == b'\n\r':
                msg.press = units.incConv_to_Pa(ret["Pressure"]) * 10 # to hpa
                msg.in_temp = units.fahrenheit_to_kelvin(ret["TempIn"])
                msg.in_humi = ret["HumIn"]
                msg.out_temp = units.fahrenheit_to_kelvin(ret["TempOut"])
                msg.out_humi = ret["HumOut"]
                msg.wind_sp = units.mph_to_m_sec(ret["WindSpeed"])
                msg.wind_dir = ret["WindDir"]
                msg.rain_rate = ret["RainRate"]
                msg.error_check = "Normal"
                rospy.loginfo(msg)
                pub.publish(msg)
            else:
                rospy.logerr("Can not access weather station")
                msg.error_check = "Error"
                pub.publish(msg)
            time.sleep(1)
        return


if __name__ == "__main__":
    davis_weather = Davis(ip = "172.20.0.40",port = 22222)
    davis_weather.pub_func()
