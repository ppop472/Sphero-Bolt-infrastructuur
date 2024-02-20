import json
import pygame
import threading
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

def load_robots_from_config():
    with open('robots_config.json', 'r') as config_file:
        config = json.load(config_file)
        toys = scanner.find_toys()
        robots = []

        for robot_config in config['robots']:
            for toy in toys:
                if robot_config['id_keyword'] in str(toy):
                    robots.append((toy, robot_config['id_keyword']))
                    break  # Break the inner loop once a matching toy is found

        return robots

def sphero_thread(toy, id_keyword, running):
    with SpheroEduAPI(toy) as sphero_api:
        sphero_api.spin(360, 1)
        sphero_api.set_heading(0)

        while running[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running[0] = False

            left_stick_x = controller.get_axis(0)
            left_stick_y = -controller.get_axis(1)
            heading = int((pygame.math.Vector2(left_stick_x, left_stick_y).angle_to(pygame.math.Vector2(1, 0)) + 90) % 360)

            print(f"Sphero with id_keyword {id_keyword} Joystick Heading:", heading)

            sphero_api.set_heading(heading)
            sphero_api.set_speed(int(abs(left_stick_y) * 100))
            sphero_api.set_speed(int(abs(left_stick_x) * 100))

            pygame.time.delay(100)

# Initialize Pygame
pygame.init()

# Set up the Xbox 360 controller
controller = pygame.joystick.Joystick(0)
controller.init()

# Load robots from config
robots = load_robots_from_config()

# Create a thread for each Sphero robot
threads = []
running = [True]  # Use a list to allow modification within the thread
for toy, id_keyword in robots:
    thread = threading.Thread(target=sphero_thread, args=(toy, id_keyword, running))
    threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()

# Main loop
while running[0]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running[0] = False

# Wait for all threads to finish
for thread in threads:
    thread.join()

print('End')
