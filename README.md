  # TERMINAL V1
  ![Picture of the Terminal](/IMAGES/terminal1.jpg)
<!-- LOGO GOES HERE
<br />
 -->
<a name="readme-top"></a>
<div align="center">
  <!--
  <a href="https://github.com/xreme/Pico-Door-Sense">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> 


 <!--<h3 align="center">Pico Door Sense</h3>-->

 <p align = "left"> 
 The Terminal is a Raspberry Pi-based project that provides users with a tactile interface for interacting with digital components.
 </p>
</div>  

 <details>
   <summary>Table of Contents</summary>
   <ol>
     <li>
       <a href="#about-the-project">About The Project</a>
     </li>
     <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#parts-list">Parts List</a></li>
        <li><a href="#software-installation">Software Installation</a></li>
        <li><a href="#wiring">Wiring</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href = "#development">Development</a></li>
    <li><a href="#acknowledgements" /> Acknowledgements</li>
   </ol>
 </details>

<!--ABOUT THE PROJECT -->
## About The Project
IoT devices are compelling pieces of technology that provide immense control and information when used correctly. IoT devices are often confined to an app or virtual assistant, often removing the physical nature of many of these devices. The terminal is aimed to add another, more tactile point of access for these devices. The terminal uses a Raspberry Pi Pico W and several other components packaged into a 3d printed enclosure to connect to the local Wi-Fi network and act as a bridge between the physical world and the virtual network in which these devices live. The terminal project also leaves room open for users to develop it further.



<!-- Getting Started -->
## Getting Started


## Parts List
1. **Main Components**
    - [Raspberry Pi Pico W][1]
    - [2x16  Serial Display][2]
    - [Beeper][3]
    - [Tactile Button][4]
    - [Rotary Encoder][5]
    - [3 LEDS (preferably different colours)][6]
    - [Prototype PCBs ][7]
2.  **Other Items**
    - Solder
    - Wire
    - Micro USB Cable
3. **Tools**
    - Soldering Iron
    - Wire Cutter & Stripper

## Software Installation

1. **Setup the Pico** -  Install the Micropython firmware onto the Raspberry Pi Pico. (<a href="https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3">Tutuorial</a>)

2. **Install the required library** - Through Thonny, install the picozero library. (<a href="https://picozero.readthedocs.io/en/latest/gettingstarted.html">documentation</a>)

3. **Load the software** -  Download the repository and copy the contents of the "terminal_code" folder onto the root directory of the Raspberry Pi Pico.

4. **Fill in network information** - Edit the "config.txt" file and replace "SSID" with your network's name and "PASSWORD" with the network password. Ensure that the network name is on the first line and the password is on the second without any spaces. 


## Wiring

_Ensure the Raspberry Pi pico is unplugged from any power before wiring._

### Rotary Encoder
|[Rotary Encoder ][5]|[Raspberry Pi Pico W][1]|
|:------------------:|:----------------------:|
|CLK                 | GP5                    |
|DT                  | GP4                    |
|+                   | GP3                    |
|SW                  | 3V3_EN                 |
|GND                 | GND                    |

### Display
|[2x16 Serial Display][2]|[Raspberry Pi Pico W][1]|
|:-----------------------|------------------------|
|SCL                | GP9                         |
|SDA                | GP8                         |
|VCC                | VBUS                        |
|GND                | GND                         |

### Other Components
| Component         | [Raspberry Pi Pico W][1]|
|:------------------|-------------------------|
| Green LED         | GP21                    |
| Yellow LED        | GP20                    |
| Red LED           | GP19                    |
| Beeper            | GP2                     |
| Push Button       | GP18                    |




## Usage

When power is supplied, the Terminal will do its initial setup and then enter its action loop; by default, the action loop will display the current time and react to any user inputs.

### Menu

The menu can be accessed by pressing the tactile button. Once taken to the menu, users can scroll through and select desired applications using the rotary encoder.

A few apps are included in the initial install; they can be hidden or removed.

### Component Testing

The testing app can then be launched via the menu under 'CMP Testing'.

The application will then walk you through testing all of the components of The Terminal.

If testing fails, please ensure all components are functional, and wires are properly connected, then try again.

### Setting the date & time

When powered on, The Terminal will display the default time. To set the correct time, users can use the menu to naviagte to the 'Set Clock' app. Within the app, users can use the push button and the rotary encoder to adjust the date and the time of The Terminal.

## Development

The code for The Terminal is completely written in MicroPython, making the development of additional applications straightforward. With this in mind, there are several things to understand:

### Pre-Loop Setup & The Action Loop

Once The Terminal is powered on, it will enter, do an initial setup and then enter the Action Loop. 

### Pre-Loop Setup

The pre-Loop Setup does several things:

**1. Initializes a _device_ object**

The _Device_ class initializes the Beeper, LEDs and LCD display in the software based on the set pinouts. The pinouts for the different components have already been set based on the above wiring tables but can switched out for different configurations.

The _Device_ class also contains several methods for interfacing with the physical components.

| Method          | args                | Description                                     |
|:---------------:|:-------------------:|:-----------------------------------------------:|
|activate         | _component_, _time_ | sets _component_ pin to high for _time_ seconds |
|display text     |_text_               | clears LCD and displays _text_                  |
|clear_display    | _clear\_display_    | clears the LCD                                  |
|sleep            | _time_              | puts the thread to sleep for _time_ seconds     |

**2. Initializes the _input drivers_ object**

The _InputDrivers_ class initializes the input components in the software based on the set pins. The pins for the inputs are preset based on the above wiring diagram. The pins can be modified for different configurations.

The _InputDrivers_ class also contains several methods for interacting with and handling user inputs:

| Method          | args                | Description                                                       |
|:---------------:|:-------------------:|:-----------------------------------------------------------------:|
|read_rotary      |                     | reads the inputs of the rotary encoder                            |
|read_button      |                     | reads the inputs of the push button                               |
|read_inputs      |                     | calls _read\_rotary_ then _read\_button_                          |
|clear_queue      |                     | clears all input-related buffers and queues                       |
|buffer_to_queue  |                     | moves user inputs from _input\_buffer_ onto the _input\_queue_    |
|input_loop       |                     | loop used to read and process user inputs (see below)             |     


**3. Initializes the _real\_time\_clock_ object**

The _real\_time\_clock_ is a class that comes standard with micropython. The _real\_time\_clock_ class is used to display and keep track of time.

**4. Starts the input loop on the second core**

The input loop is triggered by calling the _input\_driver_'s _input\_loop_ method.

The _input\_loop_ is a loop that runs on a 30-tick cycle. 

Every tick of the cycle, the following occurs:

- The loop calls the _read\_inputs_ function, which takes the user input and stores it into different arrays depending on the input type: 

  - Rotations on the rotary encoder are directly placed into the _input\_buffer_
  - Rotary Encoder presses are placed into the  _rotary\_button\_queue_
  - Button presses are placed into the _button\_queue_

- The loop calls the function _buffer\_to\_queue_ and moves all the inputs from the _input\_buffer_ to the _input\_queue_


On the last tick of every cycle, the following occurs:

- if there is a single button press within the cycle, a single button press is registered to the _input\_buffer_
- if there are two button presses (in _button\_queue_) within a cycle, a double button press is registered to _input\_buffer_
- if there are more than 4 button presses (or a button hold) within a cycle, the system will force a restart
- if there is a single rotary button press within the cycle a single button press is registered to the _input\_buffer_
- if there are two rotary button presses (in  _rotary\_button\_queue_) within a cycle, a double button press is registered to _input\_buffer_

DIAGRAM

````
Rotary Encoder turn -------------------> Input Buffer --> Input Queue
                                              ^
Rotary Encoder Press -> Rotary Button Queue->/
Push Button Press ---> Push Button queue--->/
````

### Action Loop

Once the Pre-Loop functions have completed their execution, the Terminal moves onto the Action Loop. The action loop has three main functions.

**1. Run the current application**

Every application on The Terminal contains a _run()_ function. This function allows the currently selected app to take momentary control of the system. 

**2. Set the status variables**

The _status_ variable allows for the current application to relay information back to the main loop and handle them accordingly.

**3. Read the input queue**

The input queue contains user inputs (populated by the _input\_driver_), and this function allows it to react accordingly.


### Making an Application for The Terminal

An application for The Terminal can be made in four steps.

**1. Make a new Class**

This class will store all the functions and variables needed for the application to operate. At a minimum, the class should expect the _device_ object to be an argument.

**2. Define a _run()_ function**

The _run()_ function conducts the main actions of the application. The application may call other helper functions within the _run()_ function. 

Loops may also be defined within the run function, allowing the application to take full control of the system. In these scenarios, application-specific _read\_input\_queue_ and _input\_handler_ functions should be defined.


**3.Import the application**

Import the newly created application class into the _main.py_ file. 

**4. Make the application accessible**

Within the _main.py_ file add a statement within the elif block that creates a new instance of the new application class

```
elif (application == 'New Application'):
  current_app = new_Application.NewApplication(terminal)
```

Within the _main\_menu.py_ file, add the application name to the _app\_list_.
```
self.app_list = ["Clock","Garage","Set Clock","Splash Screen","CMP Test, New Application"]
```

_Voila!_ The new application should now be accessible through The Terminal's application menu and run as expected when selected.


### Acknowledgements

The terminal makes use of darylknowles's LCD api ([found here](https://github.com/dhylands/python_lcd/blob/master/lcd/lcd_api.py))
 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<a name="Links"></a>

[1]: https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w

[2]: https://www.aliexpress.com/item/1005004934134958.html?src=google&src=google&albch=shopping&acnt=631-313-3945&slnk=&plac=&mtctp=&albbt=Google_7_shopping&gclsrc=aw.ds&albagn=888888&isSmbAutoCall=false&needSmbHouyi=false&src=google&albch=shopping&acnt=631-313-3945&slnk=&plac=&mtctp=&albbt=Google_7_shopping&gclsrc=aw.ds&albagn=888888&ds_e_adid=&ds_e_matchtype=&ds_e_device=c&ds_e_network=x&ds_e_product_group_id=&ds_e_product_id=en1005004934134958&ds_e_product_merchant_id=563759873&ds_e_product_country=CA&ds_e_product_language=en&ds_e_product_channel=online&ds_e_product_store_id=&ds_url_v=2&albcp=19373658437&albag=&isSmbAutoCall=false&needSmbHouyi=false&gad_source=1&gbraid=0AAAAACbpRIkPjvy01uAg8dufSALiP5oVC&gclid=CjwKCAjwnK60BhA9EiwAmpHZww9Ahzj_mN7H8g2812TbiUJQiaLhikfc0qXVK_5wOvb9QQYTa7qTuBoCYIgQAvD_BwE&aff_fcid=9f3f4b3935da4545b00ba110afb69964-1720487085422-08527-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=9f3f4b3935da4545b00ba110afb69964-1720487085422-08527-UneMJZVf&terminal_id=7a621ccc35954edc906e09b1404be903&afSmartRedirect=n

[3]: https://www.aliexpress.com/item/1005005394756968.html?spm=a2g0o.productlist.main.19.7cd6y1hdy1hdfv&algo_pvid=cbe81305-2821-457f-8f8f-b874e04447b2&algo_exp_id=cbe81305-2821-457f-8f8f-b874e04447b2-9&pdp_npi=4%40dis%21CAD%211.62%211.45%21%21%211.16%211.04%21%40213bdb8b17204887803183749e055e%2112000032886485069%21sea%21CA%213050193679%21&curPageLogUid=3A6BrxK3rrUe&utparam-url=scene%3Asearch%7Cquery_from%3A

[4]: https://www.aliexpress.com/item/1005004001434474.html?spm=a2g0o.productlist.main.5.2bd66763p25z7L&algo_pvid=98d04b4a-1865-48ed-9352-be63fb04fa25&algo_exp_id=98d04b4a-1865-48ed-9352-be63fb04fa25-2&pdp_npi=4%40dis%21CAD%211.81%211.81%21%21%219.45%219.45%21%40213bce9317204888315542816ede2e%2112000027701639472%21sea%21CA%213050193679%21&curPageLogUid=8lDVJWgMXe5f&utparam-url=scene%3Asearch%7Cquery_from%3A 

[5]: https://www.aliexpress.com/item/1005006127487765.html?spm=a2g0o.productlist.main.13.29da54c4FtGNex&algo_pvid=04a48268-ae55-4f1f-8689-bef1ee47751e&algo_exp_id=04a48268-ae55-4f1f-8689-bef1ee47751e-6&pdp_npi=4%40dis%21CAD%2111.56%2111.56%21%21%2160.37%2160.37%21%4021410ce717204888798514474eefc2%2112000036896392899%21sea%21CA%213050193679%21&curPageLogUid=phIfMOTGvL27&utparam-url=scene%3Asearch%7Cquery_from%3A

[6]: https://www.aliexpress.com/item/1005004272644478.html?spm=a2g0o.productlist.main.9.af40IsTJIsTJrH&algo_pvid=551ad14b-2ddf-4cd2-bab2-ee6b774cbbf5&algo_exp_id=551ad14b-2ddf-4cd2-bab2-ee6b774cbbf5-4&pdp_npi=4%40dis%21CAD%212.86%212.86%21%21%212.05%212.05%21%402101585f17204889392567553e51ac%2112000028588684694%21sea%21CA%213050193679%21&curPageLogUid=OwJkWbeU42VJ&utparam-url=scene%3Asearch%7Cquery_from%3A

[7]: https://www.aliexpress.com/item/1005006665029598.html?spm=a2g0o.productlist.main.1.7d8726b4BVigTS&algo_pvid=b7005cd8-ce68-457e-9455-b92f46ad230c&algo_exp_id=b7005cd8-ce68-457e-9455-b92f46ad230c-0&pdp_npi=4%40dis%21CAD%2126.44%218.70%21%21%21138.09%2145.44%21%402141112417204889676048705e8659%2112000037961002895%21sea%21CA%213050193679%21&curPageLogUid=xm5rTbF7CD9H&utparam-url=scene%3Asearch%7Cquery_from%3A