from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from tkinter import *
from tkinter.messagebox import *
from database import Database


class StatisticsInfo(object):
    def __init__(self):
        """创建显示统计的窗口"""
        top = Toplevel()
        self.db = Database()
        screenwidth = top.winfo_screenwidth()
        screenheight = top.winfo_screenheight()
        width = 700
        high = 600
        top.geometry('%dx%d+%d+%d' % (width, high, (screenwidth - width) / 2, (screenheight - high) / 2))

        # 创建显示数据的表格
        self.tree_view = ttk.Treeview(top, show='headings', column=('object', 'max', 'min', 'average', 'fail',
                                                                    'pass', 'middle', 'good', 'super', 'count'))
        self.tree_view.column('object', width=50, anchor="center")
        self.tree_view.column('max', width=50, anchor="center")
        self.tree_view.column('min', width=50, anchor="center")
        self.tree_view.column('average', width=50, anchor="center")
        self.tree_view.column('fail', width=50, anchor="center")
        self.tree_view.column('pass', width=50, anchor="center")
        self.tree_view.column('middle', width=50, anchor="center")
        self.tree_view.column('good', width=50, anchor="center")
        self.tree_view.column('super', width=50, anchor="center")
        self.tree_view.column('count', width=50, anchor="center")
        self.tree_view.heading('object', text='课程')
        self.tree_view.heading('max', text='最高分')
        self.tree_view.heading('min', text='最低分')
        self.tree_view.heading('average', text='平均分')
        self.tree_view.heading('fail', text='不及格')
        self.tree_view.heading('pass', text='及格')
        self.tree_view.heading('middle', text='中')
        self.tree_view.heading('good', text='良')
        self.tree_view.heading('super', text='优')
        self.tree_view.heading('count', text='总人数')

        self.tree_view.place(relx=0.02, rely=0.3, relwidth=0.96)
        self.statistics()

    def statistics(self):
        """"统计数据并显示在表格上"""
        if self.db.prepare(
                "select max(python), min(python), round(avg(python),1), count(python<60 or null), count(python<70 and "
                "python>60 or null), count(70<python and python<80 or null), count(80<python and python<90 or "
                "null), count(90<python or null), count(*) from student") != 0:
            student_tuple = self.db.cursor.fetchall()
            student_tuple = ("Python",) + student_tuple[0]
            self.tree_view.insert("", 0, values=student_tuple)
            self.db.prepare("select max(c), min(c), round(avg(c),1), count(c<60 or null), count(c<70 and "
                            "c>60 or null), count(70<c and c<80 or null), count(80<c and c<90 or "
                            "null), count(90<c or null), count(*) from student")
            student_tuple = self.db.cursor.fetchall()
            student_tuple = ("C语言",) + student_tuple[0]
            self.tree_view.insert("", 1, values=student_tuple)
            self.chart()
        else:
            showerror("统计失败", "没有学生数据无法进行统计")

    def chart(self):
        """"统计数据的柱状图"""
        # 柱状图
        # 使图形中的中文正常编码显示
        mpl.rcParams["font.sans-serif"] = ["SimHei"]
        # 每个柱子下标的索引
        self.db.prepare("select * from student")
        stu_tuple = self.db.cursor.fetchall()
        self.db.close()
        x = np.arange(len(stu_tuple))

        y = [x[2] for x in stu_tuple]
        y1 = [x[3] for x in stu_tuple]

        # 柱子的宽度
        bar_width = 0.35
        tick_label = [x[1] for x in stu_tuple]

        # 绘制柱状图并设置其各项属性
        plt.bar(x, y, bar_width, align="center", color="c", label="Python", alpha=0.5)
        plt.bar(x + bar_width, y1, bar_width, color="b", align="center", label="C语言", alpha=0.5)
        plt.tight_layout(pad=0.4, w_pad=10.0, h_pad=3.0)
        plt.title('学生成绩统计表')
        plt.xlabel("姓名")
        plt.ylabel("成绩")

        plt.xticks(x + bar_width / 2, tick_label)
        plt.xticks(rotation=-90)
        plt.yticks(np.arange(0, 101, 20))

        # 添加图例
        plt.legend(loc="upper left")

        plt.show()
