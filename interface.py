import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
import threading
import json
import tkinter as tk

def spin_robot(api, robot_id, label, move_flags):
    with api:
        time.sleep(1)
        api.spin(360, 1)
        time.sleep(1)
        api.set_heading(0)
        time.sleep(1)
        while True:
            try:
                if move_flags['w']:
                    api.set_heading(0)
                    api.set_speed(100)
                    label.config(text="W is ingedrukt")
                elif move_flags['s']:
                    api.set_heading(180)
                    api.set_speed(100)
                    label.config(text="S is ingedrukt")
                elif move_flags['a']:
                    api.set_heading(270)
                    api.set_speed(100)
                    label.config(text="A is ingedrukt")
                elif move_flags['d']:
                    api.set_heading(90)
                    api.set_speed(100)
                    label.config(text="D is ingedrukt")
                elif move_flags['b']:
                    api.spin(360,1)
                    label.config(text="spin is ingedrukt....Dance!")
                elif move_flags['q']:
                    label.config(text="Q is ingedrukt")
                    break
                elif move_flags['r']:
                    print(f"Reconnecting to Robot {robot_id}...")
                    api.reconnect()
                elif move_flags['v']:
                    api.set_heading(0)
                    api.set_speed(50)
                    time.sleep(1)
                    api.set_heading(90)
                    api.set_speed(50)
                    time.sleep(1)
                    api.set_heading(180)
                    api.set_speed(50)
                    time.sleep(1)
                    api.set_heading(270)
                    api.set_speed(50)
                    time.sleep(1)
                    api.set_heading(0)
                    time.sleep(1)
                    label.config(text="V is ingedrukt....Square!")
                    move_flags['v'] = False
                elif move_flags['c']:
                    iterations = 10
                    for i in range(iterations):
                        print("Dit is iteratie", i + 1)
                        api.set_heading(api.get_heading() + 36)
                        api.set_speed(50)
                        time.sleep(1)

                    api.set_speed(0)
                    label.config(text=f"C is ingedrukt....Circle! {iterations} turns completed.")
                    move_flags['c'] = False
                else:
                    api.roll(0, 0, 0)
                    label.config(text="Druk op een van de WASD-toetsen")

                time.sleep(0.1)

            except Exception as e:
                print(f"Error occurred: {e}")
                print(f"Connection error with Robot {robot_id}: {e}")
                print(f"Reconnecting to Robot {robot_id}...")
                api.reconnect()

def load_robots_from_config():
    with open('robots_config.json', 'r') as config_file:
        config = json.load(config_file)
        return [(SpheroEduAPI(toy), robot['id_keyword']) for toy in scanner.find_toys() for robot in config['robots'] if any(keyword in str(toy) for keyword in [robot['id_keyword']])]

def on_button_press(direction):
    move_flags[direction] = True

def on_button_release(direction):
    move_flags[direction] = False

def on_button_click(direction):
    label.config(text=f"{direction.capitalize()} button is clicked")

root = tk.Tk()
root.title("WASD Interface")

label = tk.Label(root, text="Druk op een van de WASD-toetsen")
label.pack(pady=10)

move_flags = {'w': False, 's': False, 'a': False, 'd': False, 'b': False, 'q': False, 'r': False, 'v': False, 'c': False}

button_w_frame = tk.LabelFrame(root, background="red")
button_w_frame.place(x=250, y=42)
button_w = tk.Button(button_w_frame, text="W", command=lambda: on_button_click('w'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_w.pack(side=tk.TOP)
button_w.bind("<ButtonPress>", lambda event: on_button_press('w'))
button_w.bind("<ButtonRelease>", lambda event: on_button_release('w'))

button_a_frame = tk.LabelFrame(root, background="red")
button_a_frame.place(x=100, y=200)
button_a = tk.Button(button_a_frame, text="A", command=lambda: on_button_click('a'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_a.pack(side=tk.LEFT)
button_a.bind("<ButtonPress>", lambda event: on_button_press('a'))
button_a.bind("<ButtonRelease>", lambda event: on_button_release('a'))

button_s_frame = tk.LabelFrame(root, background="red")
button_s_frame.place(x=250, y=200)
button_s = tk.Button(button_s_frame, text="S", command=lambda: on_button_click('s'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_s.pack(side=tk.BOTTOM)
button_s.bind("<ButtonPress>", lambda event: on_button_press('s'))
button_s.bind("<ButtonRelease>", lambda event: on_button_release('s'))

button_d_frame = tk.LabelFrame(root, background="red")
button_d_frame.place(x=400, y=200)
button_d = tk.Button(button_d_frame, text="D", command=lambda: on_button_click('d'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_d.pack(side=tk.RIGHT)
button_d.bind("<ButtonPress>", lambda event: on_button_press('d'))
button_d.bind("<ButtonRelease>", lambda event: on_button_release('d'))

button_b_frame = tk.LabelFrame(root, background="red")
button_b_frame.place(x=650, y=200)
button_b = tk.Button(button_b_frame, text="Spin", command=lambda: on_button_click('b'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_b.pack(side=tk.RIGHT)
button_b.bind("<ButtonPress>", lambda event: on_button_press('b'))
button_b.bind("<ButtonRelease>", lambda event: on_button_release('b'))

button_v_frame = tk.LabelFrame(root, background="red")
button_v_frame.place(x=650, y=360)
button_v = tk.Button(button_v_frame, text="Vierkant", command=lambda: on_button_press('v'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_v.pack(side=tk.RIGHT)

button_c_frame = tk.LabelFrame(root, background="red")
button_c_frame.place(x=800, y=360)
button_c = tk.Button(button_c_frame, text="Circle", command=lambda: on_button_press('c'), relief=tk.RAISED, font=("Helvetica", 16), width=10, height=5, bg="white")
button_c.pack(side=tk.RIGHT)

robots = load_robots_from_config()
threads = []

for i, (robot, robot_id) in enumerate(robots):
    print(f'Robot{i + 1} (ID: {robot_id}) movement')
    thread = threading.Thread(target=spin_robot, args=(robot, robot_id, label, move_flags))
    threads.append(thread)

for thread in threads:
    thread.start()

root.mainloop()

for thread in threads:
    thread.join()

print('End')
