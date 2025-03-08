# io_badge
IO badges for fun

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

    * Merge into a spritesheet (change the dimensions!)
        ```console
        ffmpeg -framerate 30 -i img/frames/frame_%04d.png -filter_complex "[0:v]tile=10x12" img/spritesheet.png
        ```
* This spritesheet can now be rendered in PyGame (see [example code](tests/pygame_gif.py))


<div align="center">  
 <img src="img/example.gif" width="300"> 
</div>

## Inspiration

https://www.youtube.com/watch?v=l75A9TUMXOs   
https://www.youtube.com/watch?v=mqSe_uMpxIs   
https://www.youtube.com/watch?v=cZTx7T9uwA4   
https://www.youtube.com/watch?v=GosqWcScwC0