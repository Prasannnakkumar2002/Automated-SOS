import socket
import pygame
import winsound

def play_sos_sound():
    winsound.Beep(1000, 500)

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Emergency SOS")
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.137.28", 12345)  # Replace with main laptop's IP and port
    client_socket.connect(server_address)

    sos_message = client_socket.recv(1024).decode()
    print("Received:", sos_message)

    dot_duration = 0.2
    dash_duration = 0.6
    symbol_gap_duration = 0.2
    letter_gap_duration = 0.6

    font = pygame.font.Font(None, 200)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        if running:
            play_sos_sound()
            text = font.render(sos_message, True, RED)
            screen.fill(WHITE)
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(int(dash_duration * 1000))
            screen.fill(WHITE)
            pygame.display.flip()
            pygame.time.delay(int(symbol_gap_duration * 1000))
        
    client_socket.close()
    pygame.quit()

if __name__ == "__main__":
    main()
