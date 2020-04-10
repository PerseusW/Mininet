all:
	g++ HelloWorld.cpp -o HelloWorld
	g++ Bandwidth.cpp -o Bandwidth

helloworld:
	xterm -hold -e ./HelloWorld -s -p 10000&
	sleep 1
	xterm -hold -e ./HelloWorld -c -h 127.0.0.1 -p 10000

bandwidth:
	sudo python Test.py

clean:
	rm -rf HelloWorld
	rm -rf Bandwidth
