import argparse
import networking
import networking.message
import pygame
import client.gui

def main():
    parser = argparse.ArgumentParser(description="Robot control client")
    parser.add_argument('-n', type=str, metavar='NAME', default="host", help='id used over network, first {} characters must be unique, default: host'.format(networking.message.Message.NAME_LENGTH))
    parser.add_argument('-c', action="store_true", help='is this the network client, defaults to host')
    parser.add_argument('-p', type=int, metavar='PORT', default=networking.DEFAULT_PORT, help='port to communicate over, default: {}'.format(networking.DEFAULT_PORT))
    parser.add_argument('-a', type=str, metavar='HOST', help='host name if discovery is being used and this is client')
    parser.add_argument('-d', type=int, metavar='DISCOVERY PORT', default=networking.DEFAULT_DISCOVERY_PORT, help='port to preform network discovery over, default: {}'.format(networking.DEFAULT_DISCOVERY_PORT))
    parser.add_argument('-i', type=str, metavar='DISCOVERY NAME', help='host name if discovery is being used and this is client')
    args = parser.parse_args()

    if(not args.c and not args.a is None):
        raise Warning("Host does not connect to another host")

    if args.c:
        if not args.a is None:
            networkCore = networking.Client(args.n, args.p, discoveryPort=args.d, discoveryId=args.a)
        else:
            networkCore = networking.Client(args.n, args.p, args.a)
    else:
        networkCore = networking.Server(args.n, args.p, args.d)

    pygame.init()
    mainSurface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Control 3.0")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closing")
                pygame.quit()
                networkCore.close()
            elif event.type == pygame.VIDEORESIZE:
                mainSurface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                print(event)
                    

        mainSurface.fill((255,255,255))
        pygame.draw.rect(mainSurface, (255,0,0),(150,450,100,50))
        pygame.display.update()
        clock.tick(60)
    
        