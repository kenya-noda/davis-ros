#! /usr/bin/env python3

from weather import units
import weather.stations.davis_weatherLinkIP as weatherlink
import rospy
import time
import std_msgs.msg


class Davis(object):

    def __init__(self, ip, port=22222):
        node_name = "davis"
        rospy.init_node(node_name)
        self.ip = ip
        self.port = port
        
        # Publisher definition
        self.pub_press = rospy.Publisher("/davis_press", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_intemp = rospy.Publisher("/davis_D_temp", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_inhumi = rospy.Publisher("/davis_D_humi", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_outtemp = rospy.Publisher("/davis_outside_temp", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_outhumi= rospy.Publisher("/davis_outside_humi", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_windspeed = rospy.Publisher("/davis_wind_speed", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_winddirection = rospy.Publisher("/davis_wind_direction", std_msgs.msg.Float32, queue_size = 1, latch = True)
        self.pub_rain = rospy.Publisher("/davis_rain", std_msgs.msg.Float32, queue_size = 1, latch = True)

    def pub_func(self):
        """
        Publish Function
        parse() function returns dictionary "fields"
        "fields" has some weather data, and sends "b'\n\r'" as EOL
        check EOL, and publish the weather data
        """
        while not rospy.is_shutdown():
            # connect to Vantage Pro 2
            vantage = weatherlink.VantagePro(self.ip, self.port)
            ret = vantage.parse()
            if ret["EOL"] == b'\n\r':
                self.pub_press.publish(units.incConv_to_Pa(ret["Pressure"]) * 10)
                self.pub_intemp.publish(units.fahrenheit_to_kelvin(ret["TempIn"]))
                self.pub_inhumi.publish(ret["HumIn"])
                self.pub_outtemp.publish(units.fahrenheit_to_kelvin(ret["TempOut"]))
                self.pub_outhumi.publish(ret["HumOut"])
                self.pub_windspeed.publish(units.mph_to_m_sec(ret["WindSpeed"]))
                self.pub_winddirection.publish(ret["WindDir"])
                self.pub_rain.publish(ret["RainRate"])
            else:
                print("Can not access weather station")
            time.sleep(1)
        return


if __name__ == "__main__":
    davis_weather = Davis(ip = "172.20.0.206",port = 22222)
    davis_weather.pub_func()
