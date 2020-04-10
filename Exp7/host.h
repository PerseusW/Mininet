#include <iostream>
#include <string.h>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <stropts.h>
#include <linux/netdevice.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "crc32.h"
using namespace std;

#define SIZE 1024

enum Flag {START, END, DATA, ACK, CORRUPT, TIMEOUT};

struct Packet
{
    Flag flag;
    uint32_t sequence;
    uint32_t checksum;
    char data[SIZE];
};

class Host
{
public:
    Host() {
        udpSocket = socket(PF_INET, SOCK_DGRAM, 0);
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 500000;
        setsockopt(udpSocket, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));

        memset(&SERVER, 0, sizeof(SERVER));
        SERVER.sin_family = AF_INET;

        memset(&CLIENT, 0, sizeof(CLIENT));
        CLIENT.sin_family = AF_INET;
    }

    ~Host() {
        close(udpSocket);
    }

    int sendMessageTo(const char* message, uint32_t sequence, struct sockaddr_in address, Flag flag) {
        Packet *packet = new Packet;
        packet->flag = flag;
        packet->sequence = sequence;
        strcpy(packet->data, message);
        packet->checksum = crc32(packet, sizeof(*packet));
        int result = sendto(udpSocket, packet, sizeof(*packet), 0, (struct sockaddr*)&address, sizeof(address));
        cout << "Sent: " << endl; dumpPacket(packet);
        return result;
    }

    Packet* receiveMessageFrom(struct sockaddr_in address) {
        Packet *packet = new Packet;
        packet->flag = Flag::CORRUPT;
        int result = recvfrom(udpSocket, packet, sizeof(*packet), 0, (struct sockaddr*)&SERVER, (socklen_t*)sizeof(SERVER));
        if (packet->flag == Flag::CORRUPT) {
            packet->flag = Flag::TIMEOUT;
        }
        else {
            uint32_t givenChecksum = packet->checksum;
            packet->checksum = 0;
            uint32_t calculatedChecksum = crc32(packet, sizeof(*packet));
            if (givenChecksum != calculatedChecksum) {
                packet->flag = Flag::CORRUPT;
            }
        }
        cout << "Received: " << endl; dumpPacket(packet);
        return packet;
    }

    int dumpPacket(Packet *packet) {
        cout << "  Flag: ";
        switch (packet->flag) {
            case Flag::START: cout << "START" << endl; break;
            case Flag::END: cout << "END" << endl; break;
            case Flag::DATA: cout << "DATA" << endl; break;
            case Flag::ACK: cout << "ACK" << endl; break;
            case Flag::CORRUPT: cout << "CORRUPT" << endl; break;
            case Flag::TIMEOUT: cout << "TIMEOUT" << endl; break;
        }
        cout << "  Sequence: " << packet->sequence << endl;
        cout << "  Data:" << strlen(packet->data) << endl << endl;
    }

protected:
    int udpSocket;
    struct sockaddr_in SERVER;
    struct sockaddr_in CLIENT;
};