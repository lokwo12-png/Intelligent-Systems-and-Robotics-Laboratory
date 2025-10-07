"""
main_robot.py


A sysblem that shows a robot icon moving around the screen controlled by WASD keys.
"""

import os
import sys
import pygame as py

#deine path where the robot icon will be stored.
ICON_PATH = os.path.join(os.path.dirname(__file__), "robot_icon.png")

ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/6/6b/Robot_icon.svg"

#screen setings 
SCREEN_SIZE = (640, 480) # width, height in pixels
BG_COLOR = (240, 240, 240) # light gray background
ROBOT_SIZE = (64, 64)  # width, height in pixels
ROBOT_SPEED = 200.0  # pixels per second

"""
download an image from a URL if it does not exist locally.
returns True if the image is available locally after this call.

"""
def download_icon(url, dest_path):
    if os.path.exists(dest_path):
        #skipping download, file already exists
        return True
    try:
        from urllib.request import urlopen, Request # add user-agent header to avoid 403 errors
        req = Request(url, headers={"User-Agent": "python-urllib"})
        with urlopen(req, timeout=8) as resp:
            data = resp.read()
            #save the downlaod image to the specified path
            with open(dest_path, "wb") as f:
                f.write(data)
        return True
    except Exception as e:
        print("[Non verificato] Impossibile scaricare l'icona:", e)
        return False

class RobotApp:
    """Main application class for the robot demo."""
    def __init__(self):
        # Initialize pygame and set up the window
        py.init()
        self.screen = py.display.set_mode(SCREEN_SIZE)
        py.display.set_caption("Robot WASD demo")
        self.clock = py.time.Clock()
        self.running = True

        #start robot at the center of the screen with zero velocity
        self.pos = py.math.Vector2(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        self.velocity = py.math.Vector2(0, 0)
        self.speed = ROBOT_SPEED
        
        #try to download and load the robot icon
        has_icon = download_icon(ICON_URL, ICON_PATH)
        self.robot_image = None
        if has_icon:
            try:
                img = py.image.load(ICON_PATH)
                img = py.transform.smoothscale(img, ROBOT_SIZE)
                self.robot_image = img.convert_alpha()
            except Exception as e:
                print("[Non verificato] Errore nel caricare o scalare l'immagine:", e)
                self.robot_image = None

        if self.robot_image is None:
            print("Robot image not available")

    def handle_input(self, dt):
        
        """
        check which keys are pressed and set the robot's 
        velocity accordingly. WASD keys control movement, ESC quits the app.
         """
        keys = py.key.get_pressed()
        vx = 0
        vy = 0
        if keys[py.K_a]: # move left
            vx -= 1
        if keys[py.K_d]: # move right
            vx += 1
        if keys[py.K_w]: # move up
            vy -= 1
        if keys[py.K_s]: # move down
            vy += 1
        v = py.math.Vector2(vx, vy)
        if v.length_squared() > 0:
            
        #nornalize to get speed constant in daiagonal movement
            v = v.normalize() * self.speed
        self.velocity = v
        if keys[py.K_ESCAPE]:
            self.running = False # quuit with ESC key

    def update(self, dt):
        #update the robot's position based on its velocity and keep it inside the screen bounds
        self.pos += self.velocity * dt
        w, h = ROBOT_SIZE
        self.pos.x = max(w/2, min(SCREEN_SIZE[0]-w/2, self.pos.x))
        self.pos.y = max(h/2, min(SCREEN_SIZE[1]-h/2, self.pos.y))

    def draw(self): # draw the robot and status on the screen
        self.screen.fill(BG_COLOR)
        if self.robot_image: #draw the robot icon
            rect = self.robot_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            self.screen.blit(self.robot_image, rect)
        else:
            # draw a simplre circle robot  if image is available.
            x, y = int(self.pos.x), int(self.pos.y)
            radius = min(ROBOT_SIZE)//2
            py.draw.circle(self.screen, (100, 120, 200), (x, y), radius)
            py.draw.circle(self.screen, (255,255,255), (x - radius//3, y - radius//4), radius//4)
            py.draw.circle(self.screen, (0,0,0), (x - radius//3, y - radius//4), radius//8)

        # displa text instructions and and FPS
        fps = self.clock.get_fps()
        font = py.font.SysFont(None, 20)
        lines = [
            f"WASD to move  |  ESC to quit",
            f"Position: {int(self.pos.x)},{int(self.pos.y)}  |  FPS: {int(fps)}"
        ]
        y = 8
        for line in lines:
            surf = font.render(line, True, (40,40,40))
            self.screen.blit(surf, (8, y))
            y += surf.get_height() + 2
            
        #update the display
        py.display.flip()

    def play(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # seconds per frame
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
            self.handle_input(dt)
            self.update(dt)
            self.draw()
        #quit pygame when loop ends
        py.quit()

if __name__ == '__main__':
    app = RobotApp()
    app.play()
