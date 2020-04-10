#include <string>
#include <fstream>
#include <vector>
#include "host.h"

#define CLIENT_PORT 20000

class Client: private Host
{
public:
    Client(int argc, char **argv) {
        for (int i = 0; i < argc; ++i) {
            if (strcmp(argv[i], "-f") == 0) {
                FILENAME = argv[++i];
            }
            else if (strcmp(argv[i], "-h") == 0) {
                SERVER_IP = argv[++i];
            }
            else if (strcmp(argv[i], "-p") == 0) {
                SERVER_PORT = stoi(argv[++i]);
            }
            else if (strcmp(argv[i], "-w") == 0) {
                WINDOW_SIZE = stoi(argv[++i]);
            }
        }

        struct ifconf interfaceConfiguration;
        struct ifreq interfaceRequest[50];

        interfaceConfiguration.ifc_buf = (char *)interfaceRequest;
        interfaceConfiguration.ifc_len = sizeof(interfaceRequest);

        ioctl(udpSocket, SIOCGIFCONF, &interfaceConfiguration);
        int interfaceAmount = interfaceConfiguration.ifc_len / sizeof(interfaceRequest[0]);
        char clientIP[INET_ADDRSTRLEN];
        struct sockaddr_in *s_in = (struct sockaddr_in *) &interfaceRequest[interfaceAmount - 1].ifr_addr;
        inet_ntop(AF_INET, &s_in->sin_addr, clientIP, sizeof(clientIP));

        CLIENT.sin_addr.s_addr = inet_addr(clientIP);
        CLIENT.sin_port = htons(CLIENT_PORT);
        bind(udpSocket, (struct sockaddr*)&CLIENT, sizeof(CLIENT));
        SERVER.sin_addr.s_addr = inet_addr(SERVER_IP);
        SERVER.sin_port = htons(SERVER_PORT);

        ifstream inputStream(FILENAME);
        vector<char*> fragments;
        while (inputStream) {
            char *fragment = new char[SIZE];
            inputStream.get(fragment, SIZE, '\0');
            fragments.push_back(fragment);
        }

        string clientAddress(clientIP);
        clientAddress.append(":");
        clientAddress.append(to_string(CLIENT_PORT));

        while (true) {
            sendMessageTo(clientAddress.c_str(), 0, SERVER, Flag::START);
            packet = receiveMessageFrom(SERVER);
            if (packet->flag == Flag::ACK) {
                break;
            }
        }

        uint32_t windowStart = 0, alreadySent = 0;
        while (windowStart < fragments.size()) {
            for (; alreadySent < windowStart + WINDOW_SIZE && alreadySent < fragments.size(); ++alreadySent) {
                sendMessageTo(fragments.at(alreadySent), alreadySent + 1, SERVER, Flag::DATA);
            }
            packet = receiveMessageFrom(SERVER);
            if (packet->flag == Flag::ACK) {
                windowStart = packet->sequence;
            }
            else {
                alreadySent = windowStart;
            }
        }

        for (int i = 0; i < 3; ++i) {
            sendMessageTo("", 0, SERVER, Flag::END);
            packet = receiveMessageFrom(SERVER);
            if (packet->flag == Flag::ACK && packet->sequence == 0) {
                break;
            }
        }

        inputStream.close();
    }

private:
    Packet *packet;
    char *FILENAME;
    char *SERVER_IP;
    uint32_t SERVER_PORT;
    uint32_t WINDOW_SIZE;
};

int main(int argc, char **argv)
{
    Client *client = new Client(argc, argv);
    return 0;
}