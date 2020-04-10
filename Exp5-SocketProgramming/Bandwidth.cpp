#include <iostream>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <unistd.h>
#include <chrono>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
using namespace std;

#define serverInterface "10.0.0.1"
#define threshold 1024 * 1024 * 10

class Server
{
public:
    Server(int argc, char **argv) {
        resolveArguments(argc, argv); checkArguments();
        receptionSocket = getSocketDescriber(); serverAddr = getDefaultSocketAddr();
        bind(receptionSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)); listen(receptionSocket, 5);
        
        showServerInfo();

        socklen_t socketLength = sizeof(clientAddr);
        communicationSocket = accept(receptionSocket, (struct sockaddr*)&clientAddr, &socketLength);
        
        testBandWidth(communicationSocket);

        close(receptionSocket);
        close(communicationSocket);
    }

private:
    bool serverFlag = 0;
    int port = 0; bool portFlag = 0;
    int receptionSocket = 0; struct sockaddr_in serverAddr;
    int communicationSocket = 0; struct sockaddr_in clientAddr;

    void resolveArguments(int argc, char **argv) {
        for (int i = 0; i < argc; ++i) {
            if (strcmp(argv[i], "-s") == 0) {
                serverFlag = 1;
            }
            else if (strcmp(argv[i], "-p") == 0) {
                portFlag = 1;
                port = atoi(argv[++i]);
            }
        }
    }

    void checkArguments() {
        if (!serverFlag) {
            cout << "Server argument not set" << endl;
            exit(-1);
        }
        if (!portFlag) {
            cout << "Port argument not set" << endl;
            exit(-1);
        }
        if (port < 1024 || port > 65535) {
            cout << "Invalid port number: " << port << endl;
            exit(-1);
        }
    }

    void showServerInfo() {
        cout << "Server: Listening on " << serverInterface << ":" << port << endl;
    }

    int getSocketDescriber() {
        return socket(PF_INET, SOCK_STREAM, 0);
    }

    struct sockaddr_in getDefaultSocketAddr() {
        struct sockaddr_in serverAddr;
        memset(&serverAddr, 0, sizeof(serverAddr));
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_addr.s_addr = inet_addr(serverInterface);
        serverAddr.sin_port = htons(port);
        return serverAddr;
    }

    void testBandWidth(int socket) {
        double totalBytesSent = 0;
        char testMessage[1024];

        auto startTime = chrono::steady_clock::now();
        totalBytesSent += write(socket, &startTime, sizeof(startTime));

        while (totalBytesSent < threshold) {
            totalBytesSent += write(socket, testMessage, sizeof(testMessage));
        }

        auto endTime = chrono::steady_clock::now();
        read(socket, &endTime, sizeof(endTime));

        double timeSpent = chrono::duration_cast<chrono::nanoseconds>(endTime - startTime).count() / (double)1e9;
        cout << "Server: Sent " << totalBytesSent << " bytes in " << timeSpent << " seconds" << endl;
        cout << "Server: Sent=" << totalBytesSent / (double)1024 << " KB, rate=" << totalBytesSent / 131072 / timeSpent << " Mbps" << endl;
    }
};

class Client
{
public:
    Client(int argc, char **argv) {
        resolveArguments(argc, argv); checkArguments();
        communicationSocket = getSocketDescriber(); serverAddr = getDefaultSocketAddr();
        connect(communicationSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
        
        showClientInfo();

        testBandWidth(communicationSocket);

        close(communicationSocket);
    }

private:
    bool clientFlag = 0;
    char *serverIP; bool IPFlag = 0;
    int port = 0; bool portFlag = 0;
    int communicationSocket = 0; struct sockaddr_in serverAddr;

    void resolveArguments(int argc, char **argv) {
        for (int i = 0; i < argc; ++i) {
            if (strcmp(argv[i], "-c") == 0) {
                clientFlag = 1;
            }
            else if (strcmp(argv[i], "-h") == 0) {
                IPFlag = 1;
                serverIP = argv[++i];
            }
            else if (strcmp(argv[i], "-p") == 0) {
                portFlag = 1;
                port = atoi(argv[++i]);
            }
        }
    }

    void checkArguments() {
        if (!clientFlag) {
            cout << "Client argument not set" << endl;
            exit(-1);
        }
        if (!IPFlag) {
            cout << "IP argument not set" << endl;
            exit(-1);
        }
        if (!portFlag) {
            cout << "Port argument not set" << endl;
            exit(-1);
        }
        if (port < 1024 || port > 65535) {
            cout << "Invalid port number: " << port << endl;
            exit(-1);
        }
    }

    void showClientInfo() {
        cout << "Client: Connecting to " << serverIP << ":" << port << endl;
    }

    int getSocketDescriber() {
        return socket(PF_INET, SOCK_STREAM, 0);
    }

    struct sockaddr_in getDefaultSocketAddr() {
        struct sockaddr_in serverAddr;
        memset(&serverAddr, 0, sizeof(serverAddr));
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_addr.s_addr = inet_addr(serverInterface);
        serverAddr.sin_port = htons(port);
        return serverAddr;
    }

    void testBandWidth(int socket) {
        char buffer[1024];
        double totalBytesReceived = 0;

        auto startTime = chrono::steady_clock::now();
        totalBytesReceived += read(socket, &startTime, sizeof(startTime));
        
        while (totalBytesReceived < threshold) {
            totalBytesReceived += read(socket, buffer, sizeof(buffer));
        }

        auto endTime = chrono::steady_clock::now();
        write(socket, &endTime, sizeof(endTime));

        double timeSpent = chrono::duration_cast<chrono::nanoseconds>(endTime - startTime).count() / (double)1e9;
        cout << "Client: Recv " << totalBytesReceived << " bytes in " << timeSpent << " seconds" << endl;
        cout << "Client: Recv=" << totalBytesReceived / (double)1024 << "KB, rate=" << totalBytesReceived / 131072 / timeSpent << " Mbps" << endl;
    }
};

int main(int argc, char **argv)
{
    if (argc !=  4 && argc != 6) {
		printf("Server mode: -s -p <port number>\nClient mode: -c -h <server IP address> -p <server port number>\n");
		return 0;
	}
    
    if (argc == 4) {
        Server serverMode(argc, argv);
    }
    else if (argc == 6) {
        Client clientMode(argc, argv);
    }
    else {
        return -1;
    }
    return 0;
}