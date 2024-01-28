# TAS-PF

TAS Diagram extended with Probabilistic Field.

## Explaination

This is a TAS Diagram extended with Probabilistic Field. As the wikipedia says, the TAS stands for Total Alkali Silica. The TAS can be used as a plotting diagram and a classification to assign rock type names to unlabeled igneous rocks.

The classical version of TAS is based upon the relationships between the combined alkali and silica contents and can be quite simple to use for rocks that have been chemically analyzed. 

This TAS-PF is an extended version of TAS, the PF stands for Probabilistic Field, which is generate from the GEOROC database. 

Based on the probability field obtained from the worldwide igneous data on Georoc, the probabilities are used on a case-by-case basis to determine the rock class of the samples to be classified. This approach complements the conclusions obtained from the classification boundaries in the traditional illustrations and does not perturb the classification boundaries as they may occur with the addition of data as in the traditional illustrations, and the probability field only becomes more and more stable as the size of the data grows. Thus, this project achieves both the inheritance of traditional graphical boundaries for forward compatibility and the introduction of probability fields to support data updating for backward compatibility.

## Installation

For Windows users, this TAS-PF can be installed quite easy.

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

To run this application, you should use git to clone it, with git installed and a working network. After cloning the repo, you need a working python 3.10 or above to run it.

![](./images/python_version.jpg)

And there might be some other dependencies that should be installed before moving on.

Take Ubuntu 22.04 for example, some system packages should be installed with commands below:

```Bash
sudo apt update
sudo apt install build-essential git pkg-config python3-dev python3-venv libgirepository1.0-dev libcairo2-dev gir1.2-webkit2-4.0 libcanberra-gtk3-module  libxkbcommon0 qtwayland5 libegl1-mesa
```

With no installations above, you may encounter some problems on using `pip install pycairo` and may not be able to run the beeware and related requirements.

The overall commands are like below:

```Bash
git clone https://github.com/GeoPyTool/TAS-PF.git
cd TAS-PF
pip install -r requirement.txt
```


If the requirements get installed, you may see some warnings which will not be a big problem at all.

![](./images/beeware_run.jpg)

Keep in the same path and get into the subfolder named 'taspf', then use 'briefcase run' to run it.

```Bash
cd taspf
briefcase run
```

The first time you run the commands above, you may see the second pard of requirements installation, which may take some time. 

![](./images/beeware_run.jpg)


This step will only happen on the first time you run it, next time when you run it, the downloaded requirements will be ready and there will be no need to take these time then.

![](./images/beeware_run_installation.jpg)



## Tutial

Running part will be really easy due to the simple design of TAS-PF.

### Data File Format

Both CSV and Excel files are supported by the TAS-PF.

The data file structure should be like shwon below:

![](./images/data_setting.jpg)

The required items are `Label,SiO2(wt%),K2O(wt%),Na2O(wt%)`，`Label` is required to seperate the unclassified data, the other three are the data used to plot, where `SiO2(wt%)` is used as the x , and `K2O(wt%)+Na2O(wt%)` are combined and used as y.

If you want to mannually set the plot outcome suas the colors and markers, just add the coloumns as shown above, which are in fact just the common matplotlib settings.

A sample data file can be found at [data_samples/TAS.csv](./data_samples/TAS.csv).

### Run the Application

No matter how you install it, the GUI interface will always be alomost same.

The blacnk interface will be like this:

![](./images/run_begin.jpg)

#### Open Data

Just select a CSV or Excel file and it will be loaded to the left part of the Application.

![](./images/run_data_loaded.jpg)

#### Plot Data and Export Result

When the data loaded, you may just click the `Plot Data` to do the plot and click the `Export Result` to pop up the CLassification Results. 

![](./images/run_plot_export.jpg)

The process should be so instinctive that you can figure it out very simply by exploring it.

#### Save the Result

![](./images/run_save_result.jpg)

The generated result can be added to the original data and exported as similare data file shown like [/data_samples/TAS_Result.csv](./data_samples/TAS_Result.csv)

### Switched and Effects

On the GUI, there are several switched shwon below, and the effects are also very easy to figure out.

![](./images/run_switches.jpg)

The effects are shown as pictures below.

##### Traditional Diagram

![](./images/TAS-PF-Traditional.jpg)

##### VOL with Probabilistic Field

![](./images/TAS-PF-VOL.jpg)

##### PLU with Probabilistic Field

![](./images/TAS-PF-PLU.jpg)

##### VOL with No Lines

![](./images/TAS-PF-VOL-Nolines.jpg)

##### PLU with No Lines

![](./images/TAS-PF-PLU-Nolines.jpg)

### Save the Plot

When you get satisfied with your plots, you can save it clicking the `Save Plot`.

![](./images/run_save_figure.jpg)

The plot can be save as bitmap files like PNG or JPG, and vector graphic files such like SVG or PDF.


## Acknowledgements

This project was born out of the inspiration of the late Dr. Li Jie(李解). Dr. Li was my classmate, we knew each other for more than 10 years, we used to install computers, learn programming, write software, discuss academic issues, etc. In 2023, Dr. Li died of an illness shortly after his graduation. He once criticized the idea of categorical boundaries in my early projects, which I never thought of a good way to solve. I was thinking of collaborating with him to improve it, but he has passed away. Later on, I supplemented the classification boundary idea by constructing probability fields, thus this project.

