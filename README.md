# davis-ros
	Davis社のVantage Pro2 からデータを取得し、publishするノード


## setup
	PyWeather を install します
		git clone https://github.com/kenya-noda/PyWeather.git
		pip install dist/weather-0.9.1.tar.gz
		
	ダウンロードして catkin_make
		git clone https://github.com/kenya-noda/davis-ros.git ~/ros/src/davis
		cd ~/ros
		catkin_make
		
	ip(固定) の入力
		vi ~/ros/src/davis/scripts/nanten_davis.py
    	davis_weather = Davis(ip = "~~~",port = 22222)
			
## 実行
	rosrun davis nanten_davis.py
		
