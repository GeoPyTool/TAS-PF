# TAS-PF
TAS Diagram extended with Probabilistic Field.



## Installation

### Download and Run

Download Link https://pan.baidu.com/s/1QprhPGUFd99K-4MgA9pFCA?pwd=iaiz 
Code iaiz 

This is only availiable for modern Windows system, including Windows 10 and 11.

#### Installation with MSI file on Windows

A "TAS-PF-1.0.0.msi" file is availiable in this link, which can be directly installed.

![](./images/MSI_install.jpg)


There are twon modes for this way, for current user only and for all users on the system. If you take the former way, the installed app will only be availibale for the current user who installed it.

![](./images/MSI_install_mod.jpg)

It may take about some minutes to finish the installation.

![](./images/MSI_installing.jpg)

If the installation succeced, it will tell the set wizard completed.

![](./images/MSI_installed.jpg)

Then the installed app can be found from the Start Menu.

![](./images/MSI_start.jpg)

If you do not want it installed this way anymore, you can uninstall it from the App management page.

![](./images/MSI_uninstall.jpg)


#### Unzip and run on Windows

A "TAS-PF-1.0.0.zip" file is also provided in the link above, which an be unzip to any location, where the locantion should be pure English and contain no blank in the path. 

![](./images/Zip-Unzip.jpg)

Then just go to the path you unzipped it, and you will be able to find the "TAS-PF.exe" file. Double click on this "TAS-PF.exe" file to run the application.

![](./images/Zip-ClicktoRun.jpg)

### Clone and Run 

#### Clone this repo

This way is mainly designed for Linux users and macOS users, though Windows users can also run it this way.

To run this application, you should use git to clone it, with git installed and a working network. After cloning the repo, you need a working python 3.11 or above to run it. And there might be some other dependencies that should be installed before moving on.

Take Ubuntu 22.04 for example, some system packages should be installed with commands below:

```Bash
sudo apt update
sudo apt install build-essential git pkg-config python3-dev python3-venv libgirepository1.0-dev libcairo2-dev gir1.2-webkit2-4.0 libcanberra-gtk3-module
```

The overall commands are like below:

```Bash
git clone https://github.com/GeoPyTool/TAS-PF.git
cd TAS-PF
pip install -r requirement.txt
briefcase run
```




## Tutial

### Traditional Diagram

![](./images/TAS-PF-Traditional.jpg)

### VOL with Probabilistic Field

![](./images/TAS-PF-VOL.jpg)

### PLU with Probabilistic Field

![](./images/TAS-PF-PLU.jpg)


### VOL with No Lines

![](./images/TAS-PF-VOL-Nolines.jpg)


### PLU with No Lines

![](./images/TAS-PF-PLU-Nolines.jpg)

