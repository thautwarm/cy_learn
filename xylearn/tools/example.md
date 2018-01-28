
data-helper
------------------------

简介
===============

为懒人设计的GUI数据分析。

.. image :: example.PNG

暂仅支持中文。

* TODO:

    使用imgui优化及美化GUI.
    
    添加英文、日语支持。
    
    添加更多功能。



脚本语法
===============

.. code ::

    处理文件
      <path of excel or csv> [表名为 <excel表名|csv不填>] 
    
    选取
    	<field>*
    	<new_field = any function of old ones>*
    	
    排序依据
        <field>*
    
    输出位置
    	<python expr with type string>
    
或者调用其它脚本

.. code ::
    
    读入工作计划
        <脚本文件名>*

    

案例:

.. code ::

    处理文件
      F:/xylearn/xylearn/tools/MarathonData.csv
    
    选取
    	Category
    	Name = Name.lower()
    	Marathon
    	km4week 
    	sp4week
    	scale = math.sqrt(sp4week + km4week)
    
    输出位置
    	"F:/xylearn/xylearn/tools/MarathonData2.csv"


