from manim import *  #将 manim 模块中的所有符号（类、函数等）导入
import numpy as np  #将 numpy 模块导入到当前的命名空间中，并为该模块创建了一个别名 np

class HanshuTuxiang(Scene):  #定义一个名为 HanshuTuxiang 的类，它是 Scene 类的子类
    def construct(self):  #定义了一个名为 construct 的方法，这是 Manim 中的一个特殊方法，它负责定义场景的内容
        start_color=YELLOW  #定义起始颜色为黄色 
        end_color=BLUE  #以及结束颜色为蓝色，用于在循环中创建渐变色
        axes=Axes(x_range=[-10,10,1],y_range=[-15,15,1],y_length=6,axis_config={"color":WHITE})  #创建了一个坐标轴对象 axes。它指定了 x 和 y 轴的范围（-10<x<10,-15<y<15），刻度间隔(都为1)以及 y 轴的长度（为6），并设置了坐标轴的样式（颜色设置为白色）
        self.play(Create(axes),run_time=2)  #使用 self.play()方法播放一个动画，用于创建坐标轴。Create(axes) 表示创建一个对象的动画，这里是创建坐标轴 axes。run_time=2 表示动画生成的时间为2秒
        
        for i in range(1,6):
            f=lambda x:x**i  #在每次迭代中，定义了一个函数f(x)，根据 i 的不同会生成不同的函数
            graph=axes.plot(f,color=interpolate_color(start_color,end_color,i/5))  #使用 axes.plot() 方法绘制了函数 f 的图像，并且图像的颜色使用 interpolate_color() 函数在起始颜色 start_color 和结束颜色 end_color 之间进行渐变
            label_text = f"x^{i}"  #定义标签
            graph_label =axes.get_graph_label(
                graph,
                label=MathTex(label_text),  #MathTex将字符串 label_text 渲染成数学公式
                color=interpolate_color(start_color,end_color,i/5)  #比例值 i/5 是用来控制颜色的渐变
                )  #使用 axes.get_graph_label() 方法创建了一个标签对象 graph_label，将它附加到了函数图像上
            self.play(Create(graph),Write(graph_label),run_time=2)  #播放了两个动画：一个是创建函数图像的动画，另一个是写入标签的动画，整个动画生成的时间为2秒
            self.wait()  #self.wait() 方法用于等待一段时间，便于观察最终形成的画面

class MaoPaoPaiXu(Scene):
    def construct(self):
        l=[12,6,24,3,14]  #定义了一个列表l，其中包含了待排序的数字序列
        start_color=YELLOW
        end_color=BLUE
        g=VGroup()  #创建了一个空的 VGroup 对象 g
        s=[]        #以及一个空列表 s，用于存储矩形对象
        
        for i,num in enumerate(l):
            a=Rectangle(
                height=num/10,
                width=1,
                fill_color=interpolate_color(start_color,end_color,i/len(l)),
                fill_opacity=0.5
            )  #创建了一系列矩形对象，并根据待排序的数字的大小动态调整它们的高度。同时，根据排序的进度，将矩形的填充颜色设置为渐变色，以反映当前排序的状态
            g.add(a)
            s.append(a)
        g.arrange(RIGHT, aligned_edge=DOWN)  #调整 g 中矩形对象的排列方式，使得它们按照右对齐的方式排列，并且底边对齐
        n=VGroup(*[Text(str(val)).move_to(i) for val,i in zip(l, s)])  #创建了一个包含数字标签的 VGroup 对象 n，每个数字标签对应一个矩形对象，并且与其对齐。
        self.play(Create(g),Create(n),run_time=3)  #播放动画，即创建所有的矩形对象和数字标签的过程，整个生成时间为 3 秒
        self.wait(1.5)  #等待 1.5 秒，以便观察
        
        arrow1 = Arrow(start=DOWN, end=UP, color=WHITE).next_to(s[0],DOWN)  #创建两个箭头，用于后面指示
        arrow2 = Arrow(start=DOWN, end=UP, color=WHITE).next_to(s[1],DOWN)
        self.play(Create(arrow1), Create(arrow2))
        
        for i in range(len(l)-1):  #外层循环控制比较轮数
            for j in range(len(l)-i-1):  #内层循环进行相邻元素的比较
                self.play(
                    arrow1.animate.next_to(s[j],DOWN),
                    arrow2.animate.next_to(s[j + 1],DOWN),
                    run_time=0.5  #两个箭头随着循环不断移动，分别指示正在比较的两项
                )
                if l[j]>l[j+1]:
                    s[j].generate_target()  #创建 s[j] 矩形对象的目标，用于动画中的移动
                    s[j+1].generate_target()
                    n[j].generate_target()  #创建了 n[j] 数字标签的目标，用于动画中的移动
                    n[j+1].generate_target()
                    
                    sj_bottom=s[j].get_bottom()  #获取 s[j] 矩形对象底部的位置。
                    s1j_bottom=s[j+1].get_bottom()
                    
                    s[j].target.move_to(s1j_bottom,aligned_edge=DOWN)  #将 s[j] 矩形对象的目标移动到 s[j+1] 矩形对象底部的位置，底边对齐。
                    n[j].target.move_to(s[j].target)  #将 n[j] 数字标签的目标移动到 s[j] 矩形对象的目标位置，以保持与矩形的对齐
                    s[j+1].target.move_to(sj_bottom,aligned_edge=DOWN)
                    n[j+1].target.move_to(s[j+1].target)  #以上代码生成了每次交换的动画效果，即将两个矩形对象交换位置，并相应地移动对应的数字标签
                    self.play(MoveToTarget(s[j]),MoveToTarget(s[j+1]),MoveToTarget(n[j]),MoveToTarget(n[j+1]))  #播放冒泡排序的过程
                    self.wait(0.5)
                    
                    l[j],l[j+1]=l[j+1],l[j]
                    s[j],s[j+1]=s[j+1],s[j]
                    n[j],n[j+1]=n[j+1],n[j]  #执行理论上的数字和矩形（包含标签）的交换操作，使它们按照冒泡排序的规则进行交换
        self.wait(2)

class XuanZePaiXu(Scene):
    def construct(self):
        l=[12,6,24,3,14]
        start_color=YELLOW
        end_color=BLUE
        g=VGroup()
        s=[]
        
        for i,num in enumerate(l):
            a=Rectangle(
                height=num/10,
                width=1,
                fill_color=interpolate_color(start_color,end_color,i/len(l)),
                fill_opacity=0.5
            )
            g.add(a)
            s.append(a)
        g.arrange(RIGHT, aligned_edge=DOWN)  
        n=VGroup(*[Text(str(val)).move_to(i) for val,i in zip(l, s)])
        self.play(Create(g),Create(n),run_time=3)
        self.wait(1)
        
        for i in range(len(l)):
            min_idx=l.index(min(l[i:]))  #找到未排序部分中的最小值，并获取其索引
            arrow1 = Arrow(start=DOWN, end=UP, color=WHITE).next_to(s[min_idx],DOWN)  #创建一个箭头，从下方指向最小值所在的元素
            self.play(Create(arrow1))
            
            if min_idx!=i:  #如果最小值的索引不等于当前迭代的索引 i
                self.play(arrow1.animate.next_to(s[i],DOWN),run_time=0.5)  #将箭头移动到当前迭代的元素下方
                s[i].generate_target()
                s[min_idx].generate_target()
                n[i].generate_target()
                n[min_idx].generate_target()  #以上四行用于为动画设置目标点
                
                sj_bottom=s[i].get_bottom()
                sm_bottom=s[min_idx].get_bottom()  #以上两行获取两个元素底部的坐标
                
                s[i].target.move_to(sm_bottom,aligned_edge=DOWN)
                n[i].target.move_to(s[i].target)
                s[min_idx].target.move_to(sj_bottom,aligned_edge=DOWN)
                n[min_idx].target.move_to(s[min_idx].target)  #设置元素的目标位置，将当前迭代元素移动到未排序部分的最小值位置，同时保持对齐方式为底部对齐
                self.play(MoveToTarget(s[i]),MoveToTarget(s[min_idx]),MoveToTarget(n[i]),MoveToTarget(n[min_idx]))
                self.wait(0.5)
                
                l[i],l[min_idx]=l[min_idx],l[i]
                s[i],s[min_idx]=s[min_idx],s[i]
                n[i],n[min_idx]=n[min_idx],n[i]  #交换列表中的元素及其对应的图形对象
        self.wait(2)
                   
class XianxingBianhuan(Scene):
    def construct(self):
        # 创建一个带有网格的二维坐标系（初始状态）
        initial_plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": WHITE},
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 1,
                "stroke_opacity": 1
            }
        )
        initial_plane.add_coordinates()
        # 创建一个带有网格的二维坐标系（变换后）
        transformed_plane = initial_plane.copy()
        transformed_plane.set_stroke(color=BLUE)
        # 添加初始坐标系到场景
        self.play(Create(initial_plane), run_time=2)
        # 创建原点和箭头
        origin = Dot(ORIGIN)
        vector = Arrow(start=ORIGIN, end=[1, 1, 0], buff=0, color=WHITE)
        # 创建原点和箭头的标签
        origin_label = MathTex("(0, 0)").next_to(origin, DOWN)
        vector_label = MathTex("(1, 1)").next_to(vector.get_end(), RIGHT)
        # 添加原点、箭头和标签到场景
        self.play(Create(origin), Write(origin_label), run_time=2)
        self.play(Create(vector), Write(vector_label), run_time=2)
        # 定义线性变换矩阵
        transformation_matrix = [[1, 1], [0, 1]]
        matrix_tex = MathTex(r"\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}")
        matrix_tex.to_edge(UP)
        # 添加变换矩阵到场景
        self.play(Write(matrix_tex), run_time=2)
        # 应用线性变换到新的坐标系
        self.play(
            ApplyMatrix(transformation_matrix, transformed_plane),
            ApplyMatrix(transformation_matrix, vector),
            ApplyMatrix(transformation_matrix, vector_label),
            FadeOut(vector_label),
            run_time=3
        )
        # 将变换后的坐标系添加到场景中
        self.add(transformed_plane)
        self.wait(2)
        
