# io_badge
IO badges for fun

# Hardware
- [ ] [HyperPixel2r](https://www.elektor.com/hyperpixel-2-1-round-hi-res-display-for-raspberry-pi) from Pimoroni
- [ ] Raspi Zero W
- [ ] Micro USB cable
- [ ] [USB Battery Pack](https://voltaicsystems.com/v25/)
- [ ] [3D printed case](https://a360.co/3FlakQw)
- [ ] M2.5 stads-offs, nuts and bolts

<div align="center">  
 <img src="img/cad_design.png" width="300"> 
</div>

# Installation
* Burn raspi OS [[Buster](https://downloads.raspberrypi.com/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/)] on a fresh pi
* This works best headless
    * Add a file named ```wpa_supplicant.conf``` to the BOOT folder on the sd card (not the ROOT)
        * Make sure it is encoded as EOL > Unix
        * Add the following:
            ```ini
            country=BE
            ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
            update_config=1

            network={
                ssid="SSID"
                psk="password"
                scan_ssid=1
            }
            ```
    * Add a file in the same directory called ```ssh``` (without extention, this allows to enter the pi using SSH)
    * Note to self: this didn't work on my Telenet router, but did work on the repeater
    * Enter Sd card, power up, and give the device some time to boot

* Update pi (this will take a while)
    ```console
    sudo apt update
    sudo apt upgrade -y
    ```
* Install git
    ```console
    sudo apt install git -y
    ```
* Python should be already installed. If you want to check this (& pip)
    ```console
    python3 --version
    pip3 --version
    ```
* Get the Pimeroni driver & install
    ```console
    git clone https://github.com/pimoroni/hyperpixel2r
    cd hyperpixel2r
    sudo ./install.sh
    sudo reboot
    ```
* Check boot/config.txt (or /boot/firmware/config. txt). At the end of the file, you should see
    ```ini
    # Hyperpixel configuration
    dtoverlay=hyperpixel2r
    enable_dpi_lcd=1
    dpi_group=2
    dpi_mode=87
    dpi_output_format=0x7f216
    dpi_timings=480 0 10 16 55 480 0 15 60 15 0 0 0 60 0 19200000 6
    ```
* After reboot, you should see a CLI interface on the display

* Install pygame depencies
    ```console
    sudo apt install -y python3-dev python3-pip libsdl2-dev libsmpeg-dev libportmidi-dev \
    libavformat-dev libswscale-dev libjpeg-dev libtiff5-dev libx11-6 libsdl2-net-dev
    ```
* Update pygame (you need a pygame version above 2.x)   
    (for a specific version, e.g. 2.1.3, you can use ```sudo pip3 install pygame-2.1.3-cp37-cp37m-linux_armv6l.whl```)
    ```console
    sudo apt remove python3-pygame
    sudo pip install pygame
    python3 -c "import pygame; print(pygame.__version__)"
    ```
* Reboot system
* Get the code and media directly from GitHub
    ```console
    git clone https://github.com/basbaccarne/io_badge/
    ```
* Testrun the code  
    ```console
    python3 io_badge/src/main.py
    ```

## Challenge: animated vector-based images to pygame
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

### Challenge: reducing resources on the pi
A smooth 30FPS animation based on a spritesheet can be challenging in a raspi pi zero w, which has limited resources. Paths to explore:

- [ ] Use individual images instead of spritesheet
- [ ] Use BMP instead of png
- [x] Free up system resources
    ```console
    sudo systemctl disable bluetooth
    sudo systemctl stop avahi-daemon
    sudo systemctl stop hciuart
    ```
- [x] Disable camera (```sudo raspi-config``` > Select 'Interfacing Options' -> 'Camera' -> Disable)
- [x] Increase video memory
    * ```sudo nano /boot/config.txt```
    * add ```ini gpu_mem=128```

## Inspiration

https://www.youtube.com/watch?v=l75A9TUMXOs   
https://www.youtube.com/watch?v=mqSe_uMpxIs   
https://www.youtube.com/watch?v=cZTx7T9uwA4   
https://www.youtube.com/watch?v=GosqWcScwC0