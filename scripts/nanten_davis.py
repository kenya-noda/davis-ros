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
            vantage = weatherlink.VantagePro(ip, port)
            ret = vantage.parse()
            if ret["EOL"] == b'\n\r':
                msg.press = ret["Pressure"]
                msg.in_temp = ret["TempIn"]
                msg.in_humi = ret["HumIn"]
                msg.out_temp = ret["TempOut"]
                msg.out_humi = ret["HumOut"]
                msg.wind_sp = ret["WindSpeed"]
                msg.wind_dir = ret["WindDir"]
                msg.rain_rate = ret["RainRate"]
                msg.error_check = "Normal"
                print(msg)
                pub.publish(msg)
            else:
                print("Can not access weather station")
                msg.error_check = "Error"
                pub.publish(msg)
            time.sleep(1)
        return


if __name == "__main__":
    davis_weather = Davis(ip = "",port = 22222)
    davis_weather.pub_func()
