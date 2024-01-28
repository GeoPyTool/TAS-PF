"""
TAS-PF
TAS Diagram extended with Probabilistic Field. 
一个利用概率场扩展的TAS图解软件。
版本号：1.0.0
"""
# 导入所需的库
import pkg_resources
import types
import json  # 用于处理JSON数据
import pickle  # 用于序列化和反序列化Python对象结构
import sqlite3  # 用于SQLite数据库操作
import sys  # 提供对Python运行时环境的访问
import re  # 用于正则表达式
import os  # 提供了丰富的方法来处理文件和目录
import numpy as np  # 用于科学计算

# 导入matplotlib库的部分模块，用于绘图
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from matplotlib.patches import ConnectionStyle, Polygon
from matplotlib.collections import PatchCollection
from matplotlib import collections

# 导入importlib_metadata，用于处理Python包的元数据
try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

# 导入PySide6库的部分模块，用于GUI编程
from PySide6.QtGui import QAction, QGuiApplication
from PySide6.QtWidgets import (QAbstractItemView, QMainWindow, QApplication, QMenu, QToolBar, QFileDialog, QTableView, QVBoxLayout, QHBoxLayout, QWidget, QSlider,  QGroupBox , QLabel , QWidgetAction, QPushButton, QSizePolicy)
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QVariantAnimation, Qt

# 导入matplotlib的Qt后端，用于在Qt应用程序中显示matplotlib图形
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 导入pandas，用于数据分析和操作
import pandas as pd

# 再次导入PySide6的部分模块，可能是由于代码重构或其他原因
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

# 设置matplotlib的全局配置参数

plt.rcParams['font.family'] = 'serif'  # 设置全局字体为serif类型
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']  # 设置serif类型的字体列表，优先使用'Times New Roman'
plt.rcParams['svg.fonttype'] = 'none'  # 设置在保存为SVG格式的图像时，不将文本转换为路径
plt.rcParams['pdf.fonttype'] =  'truetype'  # 设置在保存为PDF格式的图像时，使用TrueType字体

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件的目录
current_directory = os.path.dirname(current_file_path)
working_directory = os.path.dirname(current_file_path)
# 改变当前工作目录
os.chdir(current_directory)

# 定义一个自定义的PandasModel类，继承自QAbstractTableModel
class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        """
        初始化函数，接收一个pandas DataFrame对象作为参数
        :param df: pandas DataFrame对象
        :param parent: 父对象
        """
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df  # 存储DataFrame对象
        self._changed = False  # 标记数据是否已经改变
        self._filters = {}  # 存储过滤器
        self._sortBy = []  # 存储排序的列
        self._sortDirection = []  # 存储排序的方向

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        返回表头数据
        :param section: 列索引
        :param orientation: 索引的方向（水平或垂直）
        :param role: 角色
        :return: 数据或None
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]  # 返回列名
            except (IndexError,):
                return None
        elif orientation == Qt.Vertical:
            try:
                return self._df.index.tolist()[section]  # 返回索引值
            except (IndexError,):
                return None

    def data(self, index, role):
        """
        返回指定位置的数据
        :param index: 行列索引
        :param role: 角色
        :return: 数据或None
        """
        if role == Qt.DisplayRole or role == Qt.EditRole:
            try:
                return str(self._df.iloc[index.row(), index.column()])  # 返回指定位置的数据
            except:
                pass
        elif role == Qt.CheckStateRole:
            return None

        return None

    def flags(self, index):
        """
        返回指定位置的标志
        :param index: 行列索引
        :return: 项目可被选中、可被编辑的标志
        """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable  # 项目可被选中、可被编辑

    def setData(self, index, value, role=Qt.EditRole):
        """
        设置指定位置的数据
        :param index: 行列索引
        :param value: 数据值
        :param role: 角色
        :return: 设置是否成功
        """
        row = self._df.index[index.row()]  # 获取行索引
        col = self._df.columns[index.column()]  # 获取列名
        dtype = self._df[col].dtype  # 获取列的数据类型
        if dtype != object:
            value = None if value == '' else dtype.type(value)  # 如果数据类型不是object，将空字符串转换为None
        self._df.at[row, col] = value  # 设置指定位置的数据
        self._changed = True  # 标记数据已经改变
        return True

    def rowCount(self, parent=QModelIndex()):
        """
        返回行数
        :param parent: 父对象
        :return: 行数
        """
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()):
        """
        返回列数
        :param parent: 父对象
        :return: 列数
        """
        return len(self._df.columns)

    def sort(self, column, order):
        """
        对指定列进行排序
        :param column: 列索引
        :param order: 排序顺序
        """
        colname = self._df.columns.tolist()[column]  # 获取列名
        self.layoutAboutToBeChanged.emit()  # 发出布局即将改变的信号
        try:
            self._df.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)  # 对DataFrame进行排序
        except:
            pass
        try:
            self._df.reset_index(inplace=True, drop=True)  # 重置索引
        except:
            pass
        self.layoutChanged.emit()  # 发出布局已经改变的信号

# 定义一个自定义的QTableView类，继承自QTableView
class CustomQTableView(QTableView):
    # 初始化一个空的pandas DataFrame对象作为类变量
    df = pd.DataFrame()

    def __init__(self, *args):
        # 调用父类QTableView的初始化方法
        super().__init__(*args)
        
        # 设置编辑触发器为仅在双击单元格时允许编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        
        # 启用表格视图的排序功能
        self.setSortingEnabled(True)

    # 重写键盘按键事件处理函数
    def keyPressEvent(self, event):
        # 不做任何处理，直接返回
        return 

    # 重写上下文菜单事件处理函数
    def contextMenuEvent(self, event):
        # 创建一个上下文菜单对象
        contextMenu = QMenu(self)
        
        # 创建一个复制动作并添加到上下文菜单
        copyAction = QAction("Copy", self)
        contextMenu.addAction(copyAction)
        
        # 当复制动作被触发时，调用copySelection方法
        copyAction.triggered.connect(self.copySelection)
        
        # 在鼠标点击的位置显示上下文菜单
        contextMenu.exec_(event.globalPos())

    # 复制选中的数据到剪贴板的方法
    def copySelection(self):
        # 获取当前选中的所有单元格索引
        selection = self.selectionModel().selection().indexes()
        
        # 如果有选中的单元格
        if selection:
            # 计算并获取选中的行和列范围
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            
            # 创建一个与选中范围大小相同的空表格
            table = [[''] * colcount for _ in range(rowcount)]
            
            # 遍历选中的每个单元格，并将数据填入临时表格
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
                
            # 将临时表格转换为tab分隔的字符串形式，并设置到系统剪贴板
            stream = '\n'.join('\t'.join(row) for row in table)
            QGuiApplication.clipboard().setText(stream)       


# 定义一个自定义的QMainWindow类，继承自QMainWindow
class AppForm(QMainWindow):
    def __init__(self, parent=None, df=pd.DataFrame(), title='AppForm'):
        # 存储DataFrame对象
        self.df = df
        # 存储窗口标题
        self.title = title
        # 存储文件名提示
        self.FileName_Hint = title
        # 调用父类的初始化函数
        QMainWindow.__init__(self, parent)
        # 设置窗口标题
        self.setWindowTitle(self.title)
        # 创建主框架
        self.create_main_frame()

    def create_main_frame(self):
        # 设置窗口大小
        self.resize(400, 600)
        # 创建一个QWidget对象
        self.main_frame = QWidget()
        # 创建一个自定义的QTableView对象
        self.table = CustomQTableView()
        # 创建一个PandasModel对象
        model = PandasModel(self.df)
        # 设置表格视图的模型
        self.table.setModel(model)
        # 创建一个保存按钮
        self.save_button = QPushButton('&Save')
        # 当点击保存按钮时，调用saveDataFile函数
        self.save_button.clicked.connect(self.saveDataFile)
        # 创建一个垂直布局
        self.vbox = QVBoxLayout()
        # 将表格视图添加到布局
        self.vbox.addWidget(self.table)
        # 将保存按钮添加到布局
        self.vbox.addWidget(self.save_button)
        # 将布局设置为主框架的布局
        self.main_frame.setLayout(self.vbox)
        # 将主框架设置为窗口的中心部件
        self.setCentralWidget(self.main_frame)

    def saveDataFile(self):
        # 打开一个文件保存对话框，获取用户选择的文件路径
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          'Save Data File',
                                                          working_directory + self.FileName_Hint,
                                                          'CSV Files (*.csv);;Excel Files (*.xlsx)')

        # 如果DataFrame有一个名为"Label"的列，将其设置为索引
        if "Label" in self.df.columns.values.tolist():
            self.df = self.df.set_index('Label')

        # 如果用户选择了一个文件路径
        if (DataFileOutput != ''):
            # 如果文件路径的扩展名是.csv
            if ('csv' in DataFileOutput):
                # 将DataFrame保存为CSV文件
                self.df.to_csv(DataFileOutput, sep=',', encoding='utf-8')
            # 如果文件路径的扩展名是.xls或.xlsx
            elif ('xls' in DataFileOutput):
                # 将DataFrame保存为Excel文件
                self.df.to_excel(DataFileOutput)

# 定义一个名为QSwitch的自定义类，该类继承自QSlider类
class QSwitch(QSlider):
    # 初始化方法，用于构造QSwitch对象
    def __init__(self, parent=None):
        # 调用父类QSlider的初始化方法，创建一个水平方向的滑动条，并传入父窗口（可选）
        super().__init__(Qt.Horizontal, parent)
        
        # 设置滑动条的范围为0到1
        self.setRange(0, 1)
        
        # 设置滑动条的固定大小为60像素宽和20像素高
        self.setFixedSize(60, 20)

    # 重写鼠标释放事件处理函数
    def mouseReleaseEvent(self, event):
        # 首先调用父类QSlider的鼠标释放事件处理函数
        super().mouseReleaseEvent(event)
        
        # 判断滑动条当前值是否大于0.5
        if self.value() > 0.5:
            # 如果是，则将滑动条的值设置为1
            self.setValue(1)
        else:
            # 否则，将滑动条的值设置为0
            self.setValue(0)

# 定义一个自定义的QMainWindow类，继承自QMainWindow
class TAS_Extended(QMainWindow):
    def __init__(self, parent=None):
        # 调用父类的构造函数
        QMainWindow.__init__(self, parent)
        
        # 调用init_data()方法初始化数据
        self.init_data()
        
        # 调用generate_polygon()方法生成多边形
        self.generate_polygon()
        
        # 调用init_ui()方法初始化用户界面
        self.init_ui()

    def init_data(self):
        # 创建一个空的DataFrame对象来存储数据
        self.df = pd.DataFrame()
        
        # 设置默认的每英寸点数
        self.dpi = 50
        
        # 设置标签为'VOL'
        self.tag = 'VOL'
        
        # 设置设置为'Withlines'
        self.setting = 'Withlines'
        
        # 设置颜色设置为空字符串
        self.color_setting = ''
        
        # 设置数据路径为空字符串
        self.data_path = ''
    def init_ui(self):
        # 设置窗口标题和尺寸
        self.setWindowTitle('TAS-PF: TAS Diagram extended with Probabilistic Field ')
        self.resize(1024, 600)

        # 创建工具栏
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 创建主框架部件
        self.main_frame = QWidget()

        # 创建一个空的QWidget作为间隔
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 在工具栏中添加Open action
        open_action = QAction('Open Data', self)
        # 设置Open action的快捷键为Ctrl+O
        open_action.setShortcut('Ctrl+O')
        # 当Open action被触发时，调用open_file方法
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        # 在工具栏中添加Clear action
        clear_action = QAction('Clear Data', self)
        # 设置Clear action的快捷键为Ctrl+C
        clear_action.setShortcut('Ctrl+C')
        # 当Clear action被触发时，调用clear_data方法
        clear_action.triggered.connect(self.clear_data)
        toolbar.addAction(clear_action)

        # 在工具栏中添加一个Plot action
        plot_action = QAction('Plot Data', self)
        plot_action.setShortcut('Ctrl+P') # 设置快捷键为Ctrl+P
        plot_action.triggered.connect(self.plot_data)  # 连接到plot_data方法
        toolbar.addAction(plot_action)
        # 在工具栏中添加一个间隔，作为第一个开关前的分隔符
        toolbar.addWidget(spacer)

        # 在开关前添加一个标签（显示 "     VOL"）
        vol_label = QLabel("     VOL")
        toolbar.addWidget(vol_label)

        # 创建并添加一个QSwitch控件，并将其初始值设为0
        type_switch = QSwitch()
        type_switch.setValue(0)
        # 当QSwitch的状态改变时，触发toggle_vol_plu方法
        type_switch.valueChanged.connect(self.toggle_vol_plu)
        toolbar.addWidget(type_switch)

        # 在开关后添加一个标签（显示 "PLU     "）
        plu_label = QLabel("PLU     ")
        toolbar.addWidget(plu_label)

        # 添加一个间隔，作为两个开关之间的分隔符
        toolbar.addWidget(spacer)

        # 在第二个开关前添加一个标签（显示 "     With lines"）
        withlines_label = QLabel("     With lines")
        toolbar.addWidget(withlines_label)

        # 创建并添加第二个开关控件（QSwitch），初始状态为关闭（值为0）
        lines_switch = QSwitch()
        lines_switch.setValue(0)
        # 当此开关的状态发生变化时，调用toggle_lines方法进行相应处理
        lines_switch.valueChanged.connect(self.toggle_lines)
        toolbar.addWidget(lines_switch)

        # 在第二个开关控件后添加一个标签，显示 "No lines     "
        nolines_label = QLabel("No lines     ")
        toolbar.addWidget(nolines_label)

        # 添加一个间隔作为分隔符，用于将不同功能的开关区分开
        toolbar.addWidget(spacer)


        # 在第三个开关前添加一个标签，显示 "     With colors"
        withcolors_label = QLabel("     With colors")
        toolbar.addWidget(withcolors_label)

        # 创建并添加第三个开关控件（QSwitch），初始状态为关闭（值为0）
        colors_switch = QSwitch()
        colors_switch.setValue(0)
        # 当此开关的状态发生变化时，调用toggle_colors方法进行相应处理
        colors_switch.valueChanged.connect(self.toggle_colors)
        toolbar.addWidget(colors_switch)

        # 在第三个开关控件后添加一个标签，显示 "No colors     "
        nocolors_label = QLabel("No colors     ")
        toolbar.addWidget(nocolors_label)

        # 添加一个间隔，作为第三个开关后的分隔符
        toolbar.addWidget(spacer)

        # 创建并添加一个Save action到工具栏中，用于保存图表
        save_action = QAction('Save Plot', self)
        # 设置该action的快捷键为Ctrl+S
        save_action.setShortcut('Ctrl+S')
        # 当Save action被触发时，调用save_figure方法
        save_action.triggered.connect(self.save_figure)
        toolbar.addAction(save_action)

        # 创建并添加一个Export action到工具栏中，用于导出结果
        export_action = QAction('Export Result', self)
        # 设置该action的快捷键为Ctrl+E
        export_action.setShortcut('Ctrl+E')
        # 当Export action被触发时，调用export_result方法
        export_action.triggered.connect(self.export_result)
        toolbar.addAction(export_action)


        # 创建一个表格视图
        self.table = CustomQTableView()

        # 创建一个Matplotlib画布
        self.fig = Figure((10,10), dpi=self.dpi)

        self.canvas = FigureCanvas(self.fig)

        # 为canvas设置QSizePolicy，宽度拉伸，高度最小
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.canvas.setSizePolicy(sizePolicy)

        # 创建一个水平布局（将用于放置表格视图和画布）
        base_layout = QHBoxLayout()

        # 创建两个垂直布局（分别用于放置表格视图和画布）
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        # 将表格视图添加到左侧垂直布局中
        self.left_layout.addWidget(self.table)        

        # 将画布添加到右侧垂直布局中
        self.right_layout.addWidget(self.canvas)

        # 将左右两个垂直布局添加到基础的水平布局中
        base_layout.addLayout(self.left_layout)
        base_layout.addLayout(self.right_layout)

        # 将上述创建好的布局应用到主框架部件上
        self.main_frame.setLayout(base_layout)

        # 设置主框架部件为窗口的中心部件
        self.setCentralWidget(self.main_frame)

        # 显示窗口
        self.show()

    def resizeEvent(self, event):
        # 获取窗口的新大小
        new_width = event.size().width()
        # new_height = event.size().height()

        # 设置canvas的新大小，使其始终占据窗口宽度的一半
        self.canvas.setFixedWidth(new_width / 2)

        # 调用父类的resizeEvent方法，以确保其他部件也能正确地调整大小
        super().resizeEvent(event)

    def generate_polygon(self):
        self.Polygon_dict = {}
        # 获取当前文件的绝对路径
        current_file_path = os.path.abspath(__file__)

        # 获取当前文件的目录
        current_directory = os.path.dirname(current_file_path)
        
        # 改变当前工作目录到指定路径
        os.chdir(current_directory)

        # 从'tas_cord.json'文件中加载数据
        with open('tas_cord.json') as file:
            cord = json.load(file)
        # 将读取的边界线条数据存储到类实例变量self.tas_cord中
        self.tas_cord = cord

        # 绘制TAS图解的所有边界线条
        # Draw all boundary lines for the TAS diagram
        for type_label, line in cord['coords'].items():
            # 提取每条线的x坐标和y坐标
            x_coords = [point[0] for point in line]
            y_coords = [point[1] for point in line]

            # 创建一个闭合的多边形，不填充颜色，边框颜色为红色
            polygon = Polygon(list(zip(x_coords, y_coords)), closed=True, fill=None, edgecolor='r')

            # 将创建好的多边形对象存入字典中，键为type_label
            self.Polygon_dict[type_label]=polygon

    def open_file(self):
        # 获取全局变量working_directory，用于保存文件打开后的当前目录
        global working_directory

        # 弹出文件对话框，让用户选择一个CSV或Excel文件
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Files (*.csv);;Excel Files (*.xls *.xlsx)')

        # 如果用户选择了文件
        if file_name:
            # 更新工作目录为所选文件的父目录，并添加尾部斜杠
            working_directory = os.path.dirname(file_name)+'/'

            # 根据文件扩展名判断并读取数据
            if file_name.endswith('.csv'):
                self.df = pd.read_csv(file_name)  # 从CSV文件中读取数据
            elif file_name.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(file_name)  # 从Excel文件中读取数据

            # 创建一个基于DataFrame的表格模型
            model = PandasModel(self.df)

            # 将创建好的模型设置给表格视图使用
            self.table.setModel(model)  # 设置表格视图的模型

    
    def clear_data(self):
        # 清空数据
        self.df = pd.DataFrame()
        self.table.setModel(PandasModel(self.df))

        # 清空图表
        self.canvas.figure.clear()
        self.canvas.draw()


    def plot_data(self):
        if self.df.empty:
            pass
        else:
            # tag='VOL'
            # setting= 'Nolines'
            tag = self.tag
            setting = self.setting
            color_setting = self.color_setting

            # 'TAS_Base_VOL_Nolines.pkl'
            pkl_filename='TAS_Base_'+tag+'_'+setting+color_setting+'.pkl'
            # Remove the old canvas from the layout        
            # self.canvas.figure.clear()
            self.right_layout.removeWidget(self.canvas)

            # Delete the old canvas
            self.canvas.deleteLater()

            # 获取当前文件的绝对路径
            current_file_path = os.path.abspath(__file__)

            # 获取当前文件的目录
            current_directory = os.path.dirname(current_file_path)
            # 改变当前工作目录
            os.chdir(current_directory)

            # Load the Figure
            with open(pkl_filename, 'rb') as f:
                fig = pickle.load(f)
                # print('fig loaded')
            # Create a new FigureCanvas

            # Get the Axes
            ax = fig.axes[0]
            # print('ax called')


            # 创建一个空的set
            label_set = set()

            try:

                x = self.df['SiO2(wt%)']
                y = self.df['Na2O(wt%)'] + self.df['K2O(wt%)']

                # 如果self.df中没有'Color'列，根据'label'生成颜色
                if 'Color' not in self.df.columns:
                    if 'Label' in self.df.columns:
                        unique_labels = self.df['Label'].unique()
                        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
                        color_dict = dict(zip(unique_labels, colors))
                        self.df['Color'] = self.df['Label'].map(color_dict)
                    else:
                        self.df['Color'] = 'b'  # 默认颜色为蓝色
                
                # 如果self.df中没有'Marker'列，根据'label'生成符号
                if 'Marker' not in self.df.columns:
                    if 'Label' in self.df.columns:
                        unique_labels = self.df['Label'].unique()
                        markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']  # 可用的matplotlib标记
                        marker_dict = dict(zip(unique_labels, markers * len(unique_labels)))  # 如果标签数量超过标记类型，会循环使用标记
                        self.df['Marker'] = self.df['Label'].map(marker_dict)
                    else:
                        self.df['Marker'] = 'o'  # 默认符号为圆圈

                color = self.df['Color']
                marker = self.df['Marker']
                alpha = self.df['Alpha'] if 'Alpha' in self.df.columns else 0.8
                size = self.df['Size'] if 'Size' in self.df.columns else 80
                label = self.df['Label'] 

                # 获取当前ax对象中的所有数据点
                for child in ax.get_children():
                    # 检查这个子对象是否是一个散点图的集合
                    if isinstance(child, collections.PathCollection):
                        # 获取当前透明度
                        current_alpha = child.get_alpha()
                        # 获取数据点的数量
                        num_points = child.get_sizes().size
                        # 根据当前透明度和数据点的数量设置新的透明度
                        if current_alpha is not None:
                            if num_points <1000:  # 如果数据点的数量大于100
                                child.set_alpha(min(current_alpha * 2, 0.3))  # 提高透明度，但不超过1
                            elif num_points >3000:  # 如果数据点的数量小于50
                                child.set_alpha(max(current_alpha / 2, 0.005))  # 降低透明度，但不低于0.01

                def plot_group(group):
                    ax.scatter(group['x'], group['y'], c=group['color'], alpha=group['alpha'], s=group['size'], label=group.name,edgecolors='black')

                # 创建一个新的DataFrame，包含所有需要的列
                df = pd.DataFrame({
                    'x': x,
                    'y': y,
                    'color': color,
                    'alpha': alpha,
                    'size': size,
                    'marker': marker,
                    'label': label
                })

                # 按照'label'列进行分组，然后对每个组应用plot_group函数
                df.groupby('label').apply(plot_group)
                
            except KeyError:
                pass

            ax.legend()
            # Print the size of the figure
            # print('Figure size:', fig.get_size_inches())

            fig.dpi=self.dpi
            # 设置fig的尺寸为10x10
            fig.set_size_inches(10, 10)
            self.canvas = FigureCanvas(fig)

            # Add the new canvas to the layout
            self.right_layout.addWidget(self.canvas)
            # print('fig sent to canvas')
            self.canvas.draw()
            # print('canvas drawn')

    def export_result(self):   
        if self.df.empty:
            pass
        else:
            pass              
            x = self.df['SiO2(wt%)']
            y = self.df['Na2O(wt%)'] + self.df['K2O(wt%)']            
            # 创建一个函数来判断一个点是否在一个多边形内
            def point_in_polygon(point, polygon):
                return Path(polygon).contains_points([point])

            # 创建一个列表来保存所有的标签
            type_list = []
            # 遍历x和y坐标数组中的所有点对
            for x_val, y_val in zip(x, y):
                # 对于每个点，遍历字典self.Polygon_dict中存储的所有多边形及其类型标签
                for type_label, polygon in self.Polygon_dict.items():
                    # 判断当前点是否位于该多边形内
                    if point_in_polygon((x_val, y_val), polygon.get_xy()):
                        # 若点在多边形内，则从tas_cord字典的"Volcanic"键下获取与type_label对应的值，并添加到type_list列表中
                        type_list.append(self.tas_cord["Volcanic"].get(type_label))
                        # 找到符合条件的第一个多边形后跳出内层循环
                        break
                # 若点不在任何多边形内，则将None添加到type_list列表中
                else:
                    type_list.append(None)

            # 将type_list内容转换为DataFrame，设置列名为'TAS as VOL'
            tas_df = pd.DataFrame({'TAS as VOL': type_list})

            # 设置文件路径，根据self.tag变量拼接字符串得到 '_GMM_kde' 后缀的文件名部分
            file_path = self.tag + '_GMM_kde'

            # Check if the path exists
            # 检查文件路径是否存在
            if os.path.exists(file_path):
                # 遍历目录下的所有文件
                kde_result = {}
                # 将x和y数据合并为二维数组data_test
                data_test = np.column_stack((x, y))

                # 遍历指定目录中的每个文件名
                for filename in os.listdir(file_path):
                    # 提取文件名中表示目标类型的字符串（去掉"_kde.pkl"后缀）
                    type_target = filename.replace('_kde.pkl', '')
                    # 构造完整文件路径
                    full_file_path = os.path.join(file_path, filename)

                    # 以二进制模式打开并加载该文件中的pickle对象（即KDE模型）
                    with open(full_file_path, 'rb') as f:
                        kde = pickle.load(f)

                    # 创建一个用于计算概率密度的网格数据，横纵坐标范围分别为[35, 90]和[0, 20]
                    data_whole = np.column_stack((np.linspace(35, 90, 1024), np.linspace(0, 20, 1024)))

                    # 计算训练集每个点对应的对数概率密度值
                    log_whole_prob_density = kde.score_samples(data_whole)
                    # 将对数概率密度转换为原始概率密度
                    prob_density = np.exp(log_whole_prob_density)

                    # 使用KDE模型计算测试数据集的对数概率密度值
                    test_densities = kde.score_samples(data_test)

                    # 将测试数据集的对数概率密度转换为原始概率密度
                    test_probabilities = np.exp(test_densities)

                    # 计算训练集和测试集中的最大概率密度，取两者中较大的一个作为归一化基准
                    max_prob_density = max(np.max(prob_density), np.max(test_probabilities))

                    # 对测试数据集的概率密度进行归一化处理，使得所有概率密度值在0到1之间
                    test_probabilities /= max_prob_density

                    # 存储每种类型的目标对应的测试概率到字典kde_result中
                    kde_result[type_target] = test_probabilities.round(3)

                # 将字典kde_result转化为DataFrame格式
                kde_result_df = pd.DataFrame(kde_result)

                # 创建新的DataFrame来存储分类结果（最高概率对应的目标类型）
                kde_Type_df = pd.DataFrame(kde_result_df.idxmax(axis=1), columns=['Classification'])

                # 创建新的DataFrame来存储最大概率值
                kde_Probs_df = pd.DataFrame(kde_result_df.max(axis=1), columns=['Probability'])

                # 将分类结果DataFrame、概率最大值DataFrame以及其它两个预先存在的DataFrame tas_df和self.df沿列方向拼接在一起
                df = pd.concat([kde_Type_df, kde_Probs_df, tas_df, self.df], axis=1)

            # 创建一个AppForm实例，用于展示结果数据
            self.result_show = AppForm(df=df, title='TAS Result')

            # 显示该实例对应的窗口界面
            self.result_show.show()



    # 定义函数：toggle_vol_plu，接收一个布尔型参数checked
    # 功能：该方法用于根据复选框的状态切换类别显示设置，并更新图表绘制
    def toggle_vol_plu(self, checked):
        # 判断复选框是否未被选中
        if not checked:
            # 若未选中，则将tag变量设置为'VOL'
            self.tag = 'VOL'
            # 注释掉的打印语句：切换到 VOL 模式

        # 否则，判断条件取反，即复选框已被选中
        else:
            # 若已选中，则将tag变量设置为'PLU'
            self.tag = 'PLU'
            # 注释掉的打印语句：切换到 PLU 模式

        # 检查DataFrame对象self.df是否为空
        if self.df.empty:
            # 如果数据为空，则不做任何操作（pass语句）
            pass

        # 否则，若数据不为空
        else:
            # 虽然此处也无实际操作，但保留pass作为占位符，可能未来会有代码添加进来
            pass

            # 不论数据是否为空，均调用plot_data()方法重新绘制图表
            self.plot_data()

    # 定义函数：toggle_lines，接收一个布尔型参数checked
    # 功能：该方法用于根据复选框的状态切换线条显示设置，并更新图表绘制
    def toggle_lines(self, checked):
        # 如果复选框未被选中（表示要显示线条）
        if not checked:
            # 更新设置变量，指示图表中应包含线条
            self.setting = 'Withlines'
            # 注释掉的打印语句：'Switched to With Lines'

        # 如果复选框被选中（表示不应显示线条）
        else:
            # 更新设置变量，表示图表中不应有线条
            self.setting = 'Nolines'
            # 注释掉的打印语句：'Switched to No Lines'

        # 如果存储在self.df中的数据帧为空
        if self.df.empty:
            # 不进行任何操作，直接跳过当前语句
            pass

        # 如果数据帧非空
        else:
            # 虽然此处无实际操作，但保留pass作为占位符，可能未来会有代码添加进来
            pass

            # 不论数据帧状态如何，均使用更新后的设置重新绘制图表数据
            self.plot_data()

    # 定义函数：toggle_colors，接收一个布尔型参数checked
    # 功能：该方法用于根据复选框的状态切换颜色显示设置，并更新图表绘制
    def toggle_colors(self, checked):
        # 如果复选框未被选中（表示要显示颜色）
        if not checked:
            # 更新颜色设置变量，指示图表中应包含颜色
            self.color_setting = ''
            # 注释掉的打印语句：'Switched to With Colors'

        # 如果复选框被选中（表示不应显示颜色）
        else:
            # 更新颜色设置变量，表示图表中不应有颜色
            self.color_setting = '_Nocolors'
            # 注释掉的打印语句：'Switched to No Colors'

        # 如果存储在self.df中的数据帧为空
        if self.df.empty:
            # 不进行任何操作，直接跳过当前语句
            pass

        # 如果数据帧非空
        else:
            # 此处无实际操作，保留pass作为占位符，可能未来会有代码添加进来
            pass

            # 不论数据帧状态如何，均使用更新后的颜色设置重新绘制图表数据
            self.plot_data()


    # 定义函数：save_figure
    # 功能：该方法用于保存当前图表到指定的文件格式
    def save_figure(self):
        # 弹出保存文件对话框，获取用户选择的文件名
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            '保存图表',
            working_directory + 'TAS',  # 默认保存路径
            'PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;SVG Files (*.svg);;PDF Files (*.pdf)'
        )

        # 如果用户选择了文件名（即file_name非空）
        if file_name:
            try:
                # 如果文件格式为位图类型（如PNG、JPG或JPEG）
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 设置更高的DPI值（此处为默认DPI乘以10）进行保存
                    self.canvas.figure.savefig(file_name, dpi=self.dpi*10)
                else:
                    # 对于非位图格式（如SVG、PDF），使用默认DPI保存图表
                    self.canvas.figure.savefig(file_name)

            except Exception as e:
                # 如果保存过程中出现异常，打印错误信息（注释掉的实际操作部分）
                # print(f"无法保存图表: {e}")
                pass  # 程序继续执行，不因保存失败而中断

# 定义主函数：main
# 功能：初始化应用程序并启动主窗口



def main():
    # 注释：Linux桌面环境通过应用的.desktop文件将应用集成到其应用菜单中。此应用的.desktop文件包含了StartupWMClass键，设置为应用的正式名称，这有助于将应用窗口与其菜单项关联起来。
    #
    # 为了实现正确的关联，应用的所有窗口必须将其WMCLASS属性设置为与应用.desktop文件中设置的值相匹配。对于PySide2，可以通过setApplicationName()方法来设置这个值。

    # 获取启动该应用的模块名称
    app_module = sys.modules['__main__'].__package__
    # 加载应用的元数据信息
    metadata = importlib_metadata.metadata(app_module)

    # 设置应用程序的正式名称，以便与桌面环境进行窗口识别和关联
    QApplication.setApplicationName(metadata['Formal-Name'])

    # 创建一个QApplication实例
    app = QApplication(sys.argv)
    # 创建主窗口实例
    main_window = TAS_Extended()
    # 运行事件循环并退出程序，返回退出状态码
    sys.exit(app.exec())

# 检查当前模块是否为程序入口点（即直接执行的脚本）
if __name__ == '__main__':

    # 创建一个QApplication实例，用于管理图形用户界面应用程序
    app = QApplication(sys.argv)

    # 创建主窗口实例，类型为TAS_Extended类
    main_window = TAS_Extended()

    # 显示主窗口
    main_window.show()  # 这一行代码会使得窗口在屏幕上可见

    # 启动应用程序的事件循环。当事件循环结束时（例如用户关闭窗口或调用quit()方法），返回退出状态码
    sys.exit(app.exec())  # 此处的app.exec_()方法是Qt应用中启动并运行整个应用程序的关键步骤