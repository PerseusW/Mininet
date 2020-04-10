all:
	g++ client.cpp -o client
	g++ server.cpp -o server

run:
	sudo python test.py 0
	diff alice.txt test
	rm -rf test
	sleep 1
	sudo python test.py 1
	diff alice.txt test
	rm -rf test
	sleep 1
	sudo python test.py 5
	diff alice.txt test

clean:
	rm -rf client server