#include <map>
#include <fstream>
#include "host.h"

#define OUTPUT_PATH "test"

class Server: private Host
{
public:
    Server(int argc, char **argv) {
        for (int i = 0; i < argc; ++i) {
            if (strcmp(argv[i], "-d") == 0) {
                DIRECTORY = argv[++i];
            }
            else if (strcmp(argv[i], "-p") == 0) {
                SERVER_PORT = stoi(argv[++i]);
            }
            else if (strcmp(argv[i], "-w") == 0) {
                WINDOW_SIZE = stoi(argv[++i]);
            }
        }
        
        SERVER.sin_addr.s_addr = INADDR_ANY;
        SERVER.sin_port = htons(SERVER_PORT);
        bind(udpSocket, (struct sockaddr*)&SERVER, sizeof(SERVER));

        map<uint32_t, char*> data;
        uint32_t sequence;
        while (true) {
            packet = receiveMessageFrom(CLIENT);
            if (packet->flag == Flag::START) {
                sequence = packet->sequence;
                string clientAddress(packet->data);
                CLIENT.sin_addr.s_addr = inet_addr(clientAddress.substr(0, clientAddress.find(":")).c_str());
                CLIENT.sin_port = htons(stoi(clientAddress.substr(clientAddress.find(":") + 1)));
                sendMessageTo("", 0, CLIENT, Flag::ACK);
            }
            else if (packet->flag == Flag::END) {
                sendMessageTo("", 0, CLIENT, Flag::ACK);
                break;
            }
            else if (packet->flag == Flag::DATA) {
                if (packet->sequence == sequence + 1) {
                    data[sequence++] = packet->data;
                }
                sendMessageTo("", sequence, CLIENT, Flag::ACK);
            }
        }

        DIRECTORY.append(OUTPUT_PATH);
        ofstream outputStream(DIRECTORY.c_str(), ofstream::trunc);
        for (auto a: data) {
            outputStream << a.second;
        }
        outputStream.close();
    }

private:
    Packet *packet;
    string DIRECTORY;
    uint32_t SERVER_PORT;
    uint32_t WINDOW_SIZE;
};

int main(int argc, char **argv)
{
    Server *server = new Server(argc, argv);
    return 0;
}