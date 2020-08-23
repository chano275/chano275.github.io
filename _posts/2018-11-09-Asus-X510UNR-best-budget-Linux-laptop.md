---
layout: post
title: 'ASUS X510UNR : Best Budget Linux laptop'
categories: [General,]
tags : [misc, hardware, linux]
excerpt_separator: <!--more-->
---

I was at a Croma store window shopping when i happened upon this laptop,the **Asus X510UNR**.
Usually,people recommend laptops like those from the **Thinkpad** line,Dell **XPS** line and other such business class laptops for optimal **Linux** compatibility,considering they have **Intel WiFi** cards that are known to be well supported in **Linux** based systems,because Intel actively provides drivers and firmware for these cards And also because of the  high quality components,larger batteries,materials and 3 year warranty that come with these Business-class laptops

 <!--more-->

But all these however,come at a steep price,most business grade laptops start at around the **1 Lakh INR** range,with no option except to play Russian roulette with budget laptops that may not have the correct parts for an optimal Linux experience,with various incompatibilities,people on the internet seem to recommend some 5-6 year old used Thinkpads that cost about 22K INR,for running linux,and although these things are "Built like tanks" they are too old and bulky for my purposes. This is where the **Asus X510UNR** surprisingly comes in, with it's good specs and relatively cheap price of around **58K MRP**,altough i got it for around **48K INR** because of some Diwali offers Croma was running.<br>

# Specifications
<br>
<table>
    <tr><th>OS</th><td>Windows 10 Home Single Language, pre-installed</td></tr>
    <tr><th>CPU</th><td>Intel i5 8250U Quad Core processor</td></tr>
    <tr><th>RAM</th><td>8GB DDR4 SODIMM,expandable to 16GB</td></tr>
    <tr><th>iGPU</th><td>Intel HD Graphics 620</td></tr>
    <tr><th>Discrete GPU</th><td>Nvidia MX150 2GB</td></tr>
    <tr><th>Screen</th><td>15.6", Full HD 1920x1080, TN Panel, 45% NTSC color reproduction </td></tr>
    <tr><th>Storage</th><td>SATA Toshiba 1TB 5400 RPM HDD, Empty M.2 slot</td></tr>
    <tr><th>Keyboard</th><td>Centered, No Numpad,White LED Backlit</td></tr>
    <tr><th>Connectivity</th><td>Intel 8256 2x2 WiFi + BT, No Ethernet port</td></tr>
    <tr><th>Ports</th><td>HDMI, 2 x USB 2.0(Type-A), 1 x USB 3.0(Type-A), 1 x USB 3.0(USB-C), 3.5mm jack,Barrel jack for charging  and SD card reader slot</td></tr>
    <tr><th>Batteries</th><td>42 Whr, 3 cell</td></tr>

</table>

# Laptop Review

The screen is some kind of TN Panel i think, because Asus doesn't seem to mention the panel type anywhere.
It is 1080p, but color reproduction and viewing angles are bad,The default scaling lets you get more screen real estate compared to a 720p display, a boon for programmers like me.
The speakers are decent,not too low volume, not too loud,just average.
<br>
The keyboard is decent to type on, and has a backlight whose intensity can be controlled by the Function Keys, The touchpad is one of the clickable ones,with no physical left,right or middle click keys, further
the top right of the touchpad is taken up by the finger print reader.
<br>
Thermals seem to be ok,with the laptop idling at 38 C and reaching 45 C on light load,altought the laptop gets hot while charging.
<br>
By default the Windows 10 installation comes with pre-installed bloatware just like any other manufacturer, This makes no difference to me,as i run Ubuntu anyway



# Linux Compatibility

I installed **Ubuntu 18.04 LTS** on this laptop,which is my daily driver for programming and related work.<br>
My workload mainly consists of **NodeJs**, **MongoDB** and **Angular6**, all three of whose servers i have running all the time,i also use **GCC/Make** for **C** building and compilation sometimes.
<br>
The **X510UNR** is fully functional out of the box,with all the function key's alternate functions like screen brightness, keyboard backlight,audio volume,airplane mode,sleep etc all working The only packages that have to be downloaded are the **Proprietary Nvidia drivers**

```
sudo apt install nvidia-340
```

and **TLP** and **PowerTop** for battery saving

```
sudo apt install tlp powertop
```

As mentioned before, nearly everything works,but i will list them below just for convinience

- **WiFi & Bluetooth** : <span style="color: green; font-weight:400;">WORKS</span><br>
  unlike other laptops with Wifi cards from **Qualcomm** or **Realtek**,the **Intel WiFi** card works flawlessly,never once dropping connection and getting download speeds of **10 MB/s**
- **Graphics** : <span style="color: green; font-weight:400;">WORKS</span><br>
  Both the **UHD 620** and **MX150** work out of the box,with no need to set `nomodeset` while installing
- **Power Management** : <span style="color: green; font-weight:400;">WORKS</span><br>
  at around 15% brightness i can get around 5-6 hours of usage,**powertop** and **TLP** enabled,with the Nvidia GPU disabled
- **Finger Print Reader** : <span style="color: red; font-weight:400;">DOESN'T WORK</span><br>
  I have no use for a finger print reader,so this is not a deal-breaker for me
- **Audio** : <span style="color: green; font-weight:400;">WORKS</span>
- **Touchpad** : <span style="color: green; font-weight:400;">WORKS</span>
- **Camera** : <span style="color: green; font-weight:400;">WORKS</span>
- **Keyboard Backlight** : <span style="color: green; font-weight:400;">WORKS</span>
- **Function/Multimedia Keys** : <span style="color: green; font-weight:400;">WORKS</span>
- **Sleep and Wake** : <span style="color: green; font-weight:400;">WORKS</span>

<br>

**The output of `inxi -B`** :
```shell
shawn@Asus-X510U:~$ inxi -Fxs
System:    Host: Asus-X510U Kernel: 4.15.0-38-generic x86_64 bits: 64 gcc: 7.3.0
           Desktop: Unity (Gtk 3.22.30-1ubuntu1) Distro: Ubuntu 18.04.1 LTS
Machine:   Device: laptop System: ASUSTeK product: X510UNR v: 1.0 serial: N/A
           Mobo: ASUSTeK model: X510UNR v: 1.0 serial: N/A
           UEFI: American Megatrends v: X510UNR.308 date: 07/24/2018
Battery    BAT0: charge: 13.7 Wh 34.0% condition: 40.3/42.1 Wh (96%) model: ASUSTeK ASUS status: Discharging
CPU:       Quad core Intel Core i5-8250U (-MT-MCP-) arch: Kaby Lake rev.10 cache: 6144 KB
           flags: (lm nx sse sse2 sse3 sse4_1 sse4_2 ssse3 vmx) bmips: 14400
           clock speeds: max: 3400 MHz 1: 800 MHz 2: 800 MHz 3: 800 MHz 4: 800 MHz 5: 800 MHz 6: 800 MHz
           7: 800 MHz 8: 800 MHz
Graphics:  Card-1: Intel UHD Graphics 620 bus-ID: 00:02.0
           Card-2: NVIDIA GP108M [GeForce MX150] bus-ID: 01:00.0
           Display Server: x11 (X.Org 1.19.6 ) driver: i915 Resolution: 1920x1080@60.01hz
           OpenGL: renderer: Mesa DRI Intel UHD Graphics 620 (Kabylake GT2)
           version: 4.5 Mesa 18.0.5 Direct Render: Yes
Audio:     Card Intel Sunrise Point-LP HD Audio driver: snd_hda_intel bus-ID: 00:1f.3
           Sound: Advanced Linux Sound Architecture v: k4.15.0-38-generic
Network:   Card: Intel Wireless 8265 / 8275 driver: iwlwifi bus-ID: 02:00.0
           IF: wlp2s0 state: up
Drives:    HDD Total Size: 1000.2GB (1.4% used)
           ID-1: /dev/sda model: TOSHIBA_MQ04ABF1 size: 1000.2GB
Partition: ID-1: / size: 56G used: 13G (25%) fs: ext4 dev: /dev/sda5
RAID:      No RAID devices: /proc/mdstat, md_mod kernel module present
Sensors:   System Temperatures: cpu: 42.0C mobo: N/A
           Fan Speeds (in rpm): cpu: N/A
Info:      Processes: 308 Uptime: 1:45 Memory: 2009.2/7859.1MB Init: systemd runlevel: 5 Gcc sys: 7.3.0
           Client: Shell (bash 4.4.191) inxi: 2.3.56

```

# Build Quality/ Durability :

Altough this device packs all this hardware,and is yet still light,it is clear that Asus had to skimp out on the build quality of this laptop.
<br>

The plastic has this brushed metal finish on the lid,which makes it look very cheap,and is a finger-print magnet,
the chassis plastic seems flimsy and i can see a slight depression on the plastic between the 'G' and 'H' keys of the keyboard
There is a lot of flex overall, altough the laptop can be opened with one hand most of the time(a small notch is provided,like you would see on a macbook).
<br>

The venting is inadequate,with only one narrow,yet long vent at the back of the laptop,in front of the hinge,this will cause airflow issues in the future,altough for now it doesn't seem to get hot.
<br>

On the literal flipside of this though,is a removable bottom cover,which is attached to the case by around 10 screws of the Phillips #000 variety it seems, This gives you easy access to the internals of this laptop,the battery modules are sadly **glued** to the casing it seems,hindering replace-ability


# Conclusion

Overall this is a good "It-Just-Works" **Linux** laptop in this price range of **60,000 INR**, with good hardware,
<br> out-of-the-box Linux support and relative ease of maintainence and upgradability.
<br>
altough the materials and finish leave something to be desired

<span style="color: green; font-size:1.2rem; font-weight:400;">PROS</span><br>
- Latest 8th gen i5 Quad-Core processor
- Modular RAM,M2 SSD and SATA Drive slots
- Decent selection of Ports
- Light weight
- Intel Wifi
- Full HD Display
- Good out-of-the-box Linux support
- Centered Keyboard with backlight

<br>
<span style="color: red; font-size:1.2rem; font-weight:400;">CONS </span><br>
- Build quality
- Venting/Cooling
- No Ethernet port
- No Thunderbolt 3 inspite of a USB-C port
- 2x USB 2.0 Ports in 2018
- 42Whr battery
