# TAS-PF

TAS-PF：TAS Diagram extended with Probabilistic Field. 
一个利用概率场扩展的TAS图解软件。
版本号：1.0.0

## 1 简介

这是一个用概率场扩展的 TAS 图解软件。TAS 代表 Total Alkali Silica。TAS 可以用于数据投图，为未标注的火成岩指定岩石类型名称。

### 1.1 开发背景

经典版本的 TAS 是基于碱和二氧化硅总含量之间的关系进行投图判断演示类别的方法，用于判断火成岩的类型，使用起来非常简单。

TAS-PF 是 TAS 的扩展版本，PF 代表概率场，这的概率场是使用 GEOROC 数据库生成。

根据从 Georoc 全球火成岩数据中获得的概率场，逐个使用概率来确定待分类样本的岩石类别。这种方法是对传统图解中通过分类边界得出的结论的补充，不会像传统图解那样随着数据的增加而扰乱分类边界，而且概率场只会随着数据量的增加而变得越来越稳定。

本项目既继承了传统图形边界，实现了前向兼容性，又引入了概率场，支持数据更新，实现了后向兼容性。

### 1.2 开发环境

本软件的开发环境如下：

| 库名       | 版本号   | 功能描述                            |
|------------|----------|-------------------------------------|
| PySide6    | 6.6.1    | Qt 绑定库，用于 Python 的 GUI 开发    |
| beeware    | 0.3.0    | 用于原生跨平台移动和桌面应用开发工具 |
| matplotlib | 3.8.0    | 数据可视化库，绘制高质量的图表     |
| numpy      | 1.26.3   | 科学计算库，提供大量数学函数和数组操作功能 |
| pandas     | 2.1.4    | 数据分析库，提供 DataFrame 等数据结构及数据分析工具 |
| scipy      | 1.11.4   | 科学计算库，包含数值积分、优化、插值等高级数学算法 |
| toga        | 0.4.0    | Python UI 工具包，构建跨平台本地 GUI 应用程序 |
| toga-chart | 0.2.0    | Toga 库的一个扩展，用于创建图表和数据可视化组件 |
| scikit-learn | 1.2.0   | 机器学习库，包含多种监督和无监督学习算法 |

注意：不要盲目追求最新版本，比如scikit-learn，如果更新成新版本，就可能无法运行了。

### 1.3 运行环境

本软件运行所需的最低硬件配置如下：

| 配置项     | 最低要求 |
|------------|----------|
| 处理器     | 2 GHz 或更快的处理器 |
| 运行内存（RAM）   | 4 GB 以上 |
| 空闲硬盘空间   | 1 GB 以上 |
| 显示分辨率      | 1920 x 1080 分辨率 |

本软件结合PySide6与BeeWare，是一种编写跨平台GUI应用：利用PySide6构建界面，借力BeeWare的Briefcase实现一键打包和运行。此方案确保应用在Windows、GNU/Linux等几种主流操作系统上原生运行。

本软件运行所需的推荐操作系统如下：

| 操作系统   | 版本号 | 架构 | 最低版本要求 | 推荐版本要求 |
|------------|--------|------|--------------|--------------|
| Windows    | 10     | x64  | 10            | 11           |
| Linux      | Ubuntu 22.04 | x64  | Ubuntu 20.04 | Ubuntu 22.04 |

## 2 安装

对于Windows用户，安装特别简单。

### 2.1 Windows 系统下载后运行

下载链接： https://pan.baidu.com/s/1QprhPGUFd99K-4MgA9pFCA?pwd=iaiz
提取码： iaiz

需要注意的是，目前只支持主流版本的 Windows 系统，比如 Windows 10 和 11，更老的系统版本开发者本身没有，也没办法测试，所用的依赖包也无法运行了。

#### 2.1.1 Windows 系统下使用 MSI 安装包安装

上述链接中有一个 "TAS-PF-1.0.0.msi" 文件，下载后双击运行就可以安装了。

![](./images/MSI_install.jpg)

安装有两种模式，一种是只给当前用户安装，另一种是为系统环境安装。

![](./images/MSI_install_mod.jpg)

安装过程可能需要几分钟，需要一点点耐心等待。

![](./images/MSI_installing.jpg)

如果看到安装成功的提示，就是可以用了。

![](./images/MSI_installed.jpg)

安装完成之后在开始菜单里面就能找到安装好的应用了。

![](./images/MSI_start.jpg)

如果你需要移除掉已经安装的版本，去应用管理里面卸载即可。

![](./images/MSI_uninstall.jpg)

#### 2.1.2 绿色版 zip 文件解压缩运行

上面的链接中还有另外一个文件，名字为 "TAS-PF-1.0.0.zip"，这个文件下载完成后解压缩成一个独立的文件夹，然后记得存放路径一定要用英文路径，且不要有空格，否则内置解释器可能无法正常运行。

![](./images/Zip-Unzip.jpg)

保证路径没有问题之后，到解压缩的文件夹内寻找一个叫做 "TAS-PF.exe"的文件，双击这个"TAS-PF.exe"文件就可以运行程序了。

![](./images/Zip-ClicktoRun.jpg)

### 2.2 克隆代码然后运行

#### 2.2.1 克隆代码

这个运行方法主要适合 GNU/Linux 和 macOS 用户，当然 Windows 用户也可以这么运行，就是有点麻烦了。

要运行本项目的应用软件，需要使用 git 来克隆，因此要实现安装，而且还需要能够有流畅的网络，访问 github 来获取代码。克隆好代码之后，还需要一个 Python 3.10 或者以上的版本来运行克隆好的文件。

![](./images/python_version.jpg)

除了上述文件之外，还可能需要安装一些其他的系统层次的依赖包。

这里以 Ubuntu 22.04.3 为例，因为这是开发者所用的发行版本。
首先运行下面的命令安装依赖包：

```Bash
sudo apt update
sudo apt install build-essential git pkg-config python3-dev python3-venv libgirepository1.0-dev libcairo2-dev gir1.2-webkit2-4.0 libcanberra-gtk3-module  libxkbcommon0 qtwayland5 libegl1-mesa
```

如果不进行上面的步骤，后面在 `pip install pycairo` 就可能会出错，就无法完成依赖环境的完整安装。

然后克隆代码和pip安装依赖包的命令如下所示：

```Bash
git clone https://github.com/GeoPyTool/TAS-PF.git
cd TAS-PF
pip install -r requirement.txt
```

如果完成了上述的依赖包安装，就能看到类似下面的信息，有时候可能有一些 warning ，但这都不会有太大问题，只要不是 error 就基本都没事。

![](./images/beeware_run.jpg)


#### 2.2.2 运行项目

还是保持在克隆的代码的路径，然后找到子文件夹 'taspf'，利用 cd 命令进入，然后运行 'briefcase run' 就可以运行代码了。

```Bash
cd taspf
briefcase run
```

第一次运行可能需要联网更新一些程序模板等等，所以可能还需要一点时间，耐心是美德，没办法，只能等待，而且还要有一个比较稳定的网络环境，以便于访问 GitHub。

![](./images/beeware_run.jpg)


这些很耗费时间的步骤基本上只是出现在第一次运行的时候，后续的运行过程中就不会有太多类似的问题了，也会节省很多时间。

![](./images/beeware_run_installation.jpg)



## 3 操作与使用

TAS-PF的设计非常简单，所以用起来应该很容易上手

### 3.1 数据文件格式

TAS-PF 支持 CSV 和 Excel 文件，具体的设置可以参考下面的截图：

![](./images/data_setting.jpg)

必须有的列就是 `Label,SiO2(wt%),K2O(wt%),Na2O(wt%)`，`Label`就是你的样品标签， `SiO2(wt%)`和 `K2O(wt%)+Na2O(wt%)` 是你要投图的数据。

注意，这里你应该使用将所有氧化物相加然后再校准过的数据，才比较可靠。

为了简化运行流程和降低设计复杂度，TAS-PF本身不再提供数据归一化的功能，这个大家自己在Excel或者WPS上就能完成，也不麻烦。

这次的TAS-PF不需要任何额外设置，程序可以根据数据的label分组自动赋给不同的颜色，参考数据例如 [data_samples/TAS.csv](./data_samples/TAS.csv).

### 3.2 运行程序

无论是如何安装和运行，整体的图形界面都基本一样：

![](./images/run_begin.jpg)

#### 3.2.1 打开数据文件

就选择一个 CSV 或者 Excel 文件就可以加载到程序界面了。

![](./images/run_data_loaded.jpg)

#### 3.2.2 投图和判断

主界面上有 `Plot Data`和 `Export Result` 两个按钮，按前者就会生成投图，按后者就会弹出分类结果。

![](./images/run_plot_export.jpg)

这个操作流程非常直观，基本不需要什么学习成本，大家根据直觉来探索着很快就能上手。

#### 3.2.3 保存结果

![](./images/run_save_result.jpg)

弹出的判断结果表格可以保存成一个文件，可以参考 [/data_samples/TAS_Result.csv](./data_samples/TAS_Result.csv)，实际就是在源数据文件的左侧加上概率场判断类别、判断概率、TAS经典图解判断类别这三列。

### 3.3 切换效果

在图形界面上，可以在VOL和PLU之间切换GEOROC底图数据，另外还可以切换是否显示线条，还有对底图显示的开关。

![](./images/run_switches.jpg)

具体效果如下所示：

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

### 3.4 保存投图

经过一番调整之后，如果你想要保存下来当前投图，就可以点击 `Save Plot`，如下图所示：

![](./images/run_save_figure.jpg)

该程序提供了四种保存格式：JPG和PNG两种是位图，PDF和SVG两种是矢量图。大家如果用CorelDraw或者Adobe Illustrator，推荐使用PDF。如果使用 Ink Scape 或者 Affinity Designer，推荐使用 SVG。


## 4 致谢

这个项目的灵感源于已故的李解博士。李解博士是我的同班同学，我们相识十多年，经常一起装电脑、学编程、写软件、讨论学术问题。2023 年，李博士毕业后不久不幸因病去世。他曾经批评过我早期项目中的分类界限思想，我一直没有想到好的解决方法。本想与他合作改进，但他已经去世了。后来，我通过构建概率场来补充分类边界的想法，于是就有了这个项目。
