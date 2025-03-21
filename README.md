# IO Badge
This project explores the possibilities of integrating a circular display with a raspberry pi zero W in an integrated set-up. Current use case: interactive badges that can be used to show off 🕶️.

# Hardware
- [ ] [HyperPixel2r](https://www.elektor.com/hyperpixel-2-1-round-hi-res-display-for-raspberry-pi) from Pimoroni
- [ ] [Raspi Zero WH2](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) (the H version has headers)
- [ ] Micro USB to USB A cable (power)
- [ ] [USB Battery Pack](https://voltaicsystems.com/v25/) // to be explored: Lipo + [LiPo Rider](https://www.kiwi-electronics.com/en/lipo-rider-plus-charger-booster-5v-2-4a-usb-type-c-9960)
- [ ] [3D printed case](https://a360.co/3FlakQw) (be carefull not to break your SD card when mounting, I've been there)
- [ ] [M2.5 stand-offs, nuts and bolts](https://www.adafruit.com/product/3299)
- [ ] M2.5 threaded inserts
- [ ] [4 Rare Earth Magnets](https://www.kiwi-electronics.com/nl/high-strength-rare-earth-magnet-3203)

<div align="center">  
 <img src="img/cad_design.png" width="300"> 
</div>

# Installation
* Burn raspi OS on a fresh pi
* This works best headless (setup eveything in the raspberry pi burner to connect using SSH and connect to the wifi)
   <details>
     <summary> Or use this manual approach</summary>   
    
        * Add a file named wpa_supplicant.conf to the BOOT folder on the sd card (not the ROOT)
           * Make sure it is encoded as EOL > Unix
           * Add the following:
               
               country=BE
               ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
               update_config=1
               ap_scan=1  
   
               network={
                   ssid="SSID"
                   psk="password"
                   scan_ssid=1
                   key_mgmt=WPA-PSK
               }
               
       * Add a file in the same directory called ssh (without extention, this allows to enter the pi using SSH)
       * Note to self: this didn't work on my Telenet router, but did work on the repeater
     </details>
    

* Enter SD card in Pi, power up, and give the device some time to boot (reboot can be needed after initial boot)
* I like to use my phone's hotspot for this, use Angry IP scanner for IP adresses and WinSCP/Putty for SSH or in cmd
  ```console
   ssh pi@[ip.adress]
  ```
* Update pi (this will take a while)
    ```console
    sudo apt update
    sudo apt upgrade -y
    ```
* Python, pip & pygame should be already installed. If you want to check this
    ```console
    python3 --version
    pip3 --version
    python3 -c "import pygame; print(pygame.__version__)"
    ```
* Install the Pimoroni display
    ```console
    sudo nano /boot/firmware/config.txt
    ```
    * add ```dtoverlay=vc4-kms-dpi-hyperpixel2r``` at the end of the document
    * configurations (```sudo raspi-config```)
      * enable I2C
      * set to boot in CLI
* Reboot
* Get the code and media directly from GitHub
    ```console
    git clone https://github.com/basbaccarne/io_badge/
    ```
* Testrun the pygame code (simple) 
    ```console
    python3 io_badge/tests/pygame_simple.py
    ```
* Install MPV (to play movies) & test
    ```console
    sudo apt install mpv -y
    mpv --fs --loop=inf /home/pi/io_badge/img/test_optimized.mp4
    ```    
* Testrun the main code (python script that runs the required services)
    ```console
    python3 io_badge/src/main.py
    ```
* set-up **auto boot**
   * Create service
     ```console
     sudo nano /etc/systemd/system/videoplayer.service
     ```
   * Add this code
     ```ini
     [Unit]
     Description=Autostart Video Player on Boot (Framebuffer)
     After=multi-user.target
     Wants=multi-user.target
     
     [Service]
     User=pi
     Group=pi
     Type=simple
     Environment="XDG_RUNTIME_DIR=/run/user/1000"
     ExecStart=/usr/bin/mpv --fs --loop=inf /home/pi/io_badge/img/test_optimized.mp4
     WorkingDirectory=/home/pi
     Restart=always
     RestartSec=5
     Environment=DISPLAY=:0
     TTYPath=/dev/tty1
     
     [Install]
     WantedBy=multi-user.target
     ```
  * Enable the service
    ```console
    sudo systemctl daemon-reload
    sudo systemctl enable videoplayer.service
    sudo systemctl start videoplayer.service
    ```

## Subchallenge: playing visuals on a raspberry pi zero W

Visualising animations on this set-up can be done in 4 ways.

* mpv (best performance for videos)
* fbi (image sequences)
* pygame (interactive image sequences)
* PIL (ultra lightweight rendering)

### mpv   

**Create video**   
You can create videos from e.g. protopie (click record in the preview window to save as mp4).    

**Optimize video**   
resolution of 480x480, 30 FPS, no sound, ultrafast, bitrate of 30 (don't do this if you need acurate colors)   

```console
ffmpeg -i img/test.mp4 -vf "scale=480:480,fps=30" -c:v libx264 -preset ultrafast -crf 30 -an img/test_optimized.mp4
```

**Play the video**   
You can play this video with mpv (install if needed)   

```console
sudo apt install mpv -y
mpv --fs --loop=inf /home/pi/io_badge/img/test_optimized.mp4
```

## Subchallenge: animated vector-based images to pygame
Let's start at the beginning. If we want to create an animation, we need to first design and animate a concept. I believe that Figma has the best balance between creative flexibility and intuitive controls. For more advanced animations you can work in Adobe After Effects, Krita, etc. 

**Animations in Figma**
* Create animations by using frames that are interconnected using small delays and smart animations (elements with the same name are interpreted as the same element) [[sample](https://www.figma.com/design/7HCxisRHbDd5nCdcb7xBon/animation?node-id=0-1&t=ho44WM4fuoWQwnLI-1)].
* Activiate the Lottefiles plugin and upload the flow to Lottie [[sample](https://lottiefiles.com/free-animation/example-ibx1J4zz1J)].
* download the lottefile as a GIF in the original size (set required framerate). On low resource systems, low framerates are recommended [[sample, 30 FPS](/img/example.gif)].

**Animated GIFs in Python**
* PyGame can be a bit though in handling animations.
* The most resource effective way is to create ````spritesheet```` with the individual frames of the animation
* A good solution is to do this using ```FFmpeg```   

    (you might need to restart the terminal after installation)   
    (the 'frames' folder must exist)

    * Split the gifs in individual PNGs

        ```console
        winget install ffmpeg
        ffmpeg -i img/example.gif img/frames/frame_%04d.png
        ```

    * Merge into a spritesheet (change the dimensions, beware: ffpmpeg has filesize limits!)
        ```console
        ffmpeg -framerate 30 -i img/frames/frame_%04d.png -filter_complex "[0:v]tile=10x12" img/spritesheet.png
        ```
* This spritesheet can now be rendered in PyGame (see [example code](tests/pygame_gif.py))


<div align="center">  
 <img src="img/example.gif" width="300"> 
</div>

However, rendering in PyGame on a raspi zero is challenging and should be kept to a minimum. Preferably only when interaction is needed.   

### Subchallenge: reducing resources on the pi
A smooth 30FPS animation based on a spritesheet can be challenging in a raspi pi zero w, which has limited resources, even on a zero W2 the FPS for full screen 480x480 pngs in a spritesheet is a bit too munch. Paths to explore:
- [x] Free up system resources 
    ```console
    sudo systemctl disable bluetooth
    sudo systemctl stop avahi-daemon
    sudo systemctl stop hciuart
    ```
    
    ```Verdict```: still too slow

- [x] Disable camera (```sudo raspi-config``` > Select 'Interfacing Options' -> 'Camera' -> Disable)

   ```Verdict```: still too slow

- [x] Increase video memory
    * ```sudo nano /boot/config.txt```
    * add ```ini gpu_mem=128```
      
   ```Verdict```: still too slow

- [x] animated GIF directly ([test script](tests/pygame_directgif.py))

  ```console   
  pip install pillow
  ``` 
  ```Verdict```: still too slow

- [x] Use individual images instead of spritesheet (png) ([tests script](tests/pygame_individualpngs.py))
      
  ```Verdict```: still too slow, but significantly better

- [x] Use BMP instead of png

  ```console
  ffmpeg -i img/example.gif img/frames/frame_%04d.bmp
  ```

  ```Verdict```: still too slow

**CONCLUSION:** running animated GIFs in pygame is challenging on a raspi zero w 2. Running video's works, for for PyGame it is better design in PyGame as much as possible and to keep it as simple as possible. 

## Subchallenge: raspi and Lipo batteries
For a wireless badge, I want to include a Lipo battery pack to power the raspi and the screen. To do this, I'm experimenting with the [Seeed Studio Lipo rider](https://wiki.seeedstudio.com/Lipo-Rider-Plus/) plus (you only need the pro version if you want to work with something like solar panels). This not only includes easy charging but also has a switch that we can use to power up and down our device (both physical and pin controlled).

* Output: 5V / 4.4A (can also output 3.3V/250mA)
* Required: raspi under load (600mA) + display (110mA backlight + 40mA screen) = 270 mA > provide min. 1A
* Battery ranges:
   * 1-3 hours: 2500-3000mAh
   * 4-6 hours: 4000-6000mAh
   * 8+ hours: 10000mAh
 
 Embedding this in a product:
 - [ ] a lot of **heath** will build up with all these electronics: think about ventillation or use thermal pads on the Pi's CPU
 - [ ] Include a button to control the power (e.g. an extention of the physical button)
 - [ ] Work with light guides to transfer led power on led and battery level leds

## Inspiration

https://www.youtube.com/watch?v=l75A9TUMXOs   
https://www.youtube.com/watch?v=mqSe_uMpxIs   
https://www.youtube.com/watch?v=cZTx7T9uwA4   
https://www.youtube.com/watch?v=GosqWcScwC0
