# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 11:03:20 2018

@author: thautwarm
"""

from tkinter import Scrollbar, Tk, END, Button, Text, filedialog, N, S, E, W
import os
from collections import defaultdict
import pandas as pd
import time
import base64
from linq.standard.general import GroupBy, Map, Filter

# Icon
with open("./tmp.ico", "wb") as tmp, open('image', 'rb') as img:
    tmp.write(base64.b64decode(img.read()))

# Constants
indent = "      "
BEGIN = "1.0"  # Tkinter beginning marker.
CHINESEFONT = 'FangSong'
BOM = "\ufeff"
CodecList = ('utf8', 'gbk')


def parse(text: str):
    """naive parser for the script we use here.
    """
    cell_head = None
    cell = defaultdict(list)
    for line in text.splitlines():
        line: str
        if line.startswith(BOM):
            line = line.strip(BOM)
        if not line:
            continue
        if line.startswith(' ') or line.startswith('\r\t') or line.startswith('\t'):
            cell[cell_head].append(line.strip())
        else:
            cell_head = line.strip()
    return cell


def call_open_filenames(manager):
    def callback():
        filename_text = ("处理文件"
                         f"\n{indent}"
                         "{}\n".format(
            f'\n{indent}'
                .join(Filter
                      (filedialog.askopenfilenames()))))

        manager.editor.insert(BEGIN, filename_text)

    return callback


def load_script(manager):
    def callback():
        """Load script codes from specific files.
        """
        filename = filedialog.askopenfilename()

        if not filename:
            return

        for encoding in CodecList:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    string = f.read()
                    manager.editor.delete(BEGIN, END)
                    manager.editor.insert(BEGIN, string)
                    break
            except UnicodeDecodeError:
                continue

    return callback


def remove_undef_col(old: pd.DataFrame):
    """Remove `Unnamed` fields. 
    """
    return old.loc[:, [_ for _ in old.columns if not _.startswith('Unnamed')]]


def read_data(file_and_table):
    if len(file_and_table) is 1:
        file: str = file_and_table[0]
        return pd.read_csv(file) if file.lower().endswith('.csv') else pd.read_excel(file)
    return pd.read_excel(file_and_table[0], sheetname=file_and_table[1])


def write_date(df, filename):
    for encoding in CodecList:
        try:
            (lambda df: getattr(df,
                                ['to_excel', 'to_csv'
                                 ][int(filename.endswith('.csv'))]
                                )(filename, encoding=encoding))(df)
        except UnicodeEncodeError:
            continue


class Manager:
    def __init__(self, log_path=os.path.abspath('./')):

        root = Tk()
        root.title('grouping-helper')
        root.geometry()
        root.iconbitmap('tmp.ico')
        os.remove("./tmp.ico")

        # UI Layers
        editor = Text(root, height=20, width=50, font=CHINESEFONT)
        console = Text(root, height=20, width=30, font=CHINESEFONT)
        src_editor = Scrollbar(root, command=editor.yview)
        scr_console = Scrollbar(root, command=editor.yview)
        editor.configure(yscrollcommand=src_editor.set)
        console.configure(yscrollcommand=scr_console.set)

        select_file_btn = Button(root,
                                 command=call_open_filenames(self),
                                 text='选择数据')

        self.load_script = Button(root,
                                  command=load_script(self),
                                  text="导入工作计划")
        self.run_btn = Button(root,
                              command=self.run,
                              text='生成结果')

        self.select_file_btn = select_file_btn
        self.console = console
        self.editor = editor
        self.root = root
        self.src_editor = src_editor
        self.scr_console = scr_console
        self.log_path = log_path
        self.display()

    def run(self):
        text = self.editor.get(BEGIN, END)
        parsed: dict = parse(self.editor.get(BEGIN, END))

        # logging
        for encoding in CodecList:
            try:
                with open(f'{self.log_path}/日志.txt', 'a+', encoding=encoding) as f:
                    f.write('\n' + time.ctime() + '\n')
                    f.write(text)
                    break
            except UnicodeDecodeError:
                continue

        self.console.delete(BEGIN, END)
        if parsed['读入工作计划']:
            self.console.insert(END, "读入外部工作计划。\n")
            items = parsed['读入工作计划']
            for item in items:
                for encoding in CodecList:
                    try:
                        with open(item, 'r', encoding=encoding) as f:
                            self.interpret(parse(f.read()))
                        break
                    except UnicodeDecodeError:
                        continue
        else:
            self.interpret(parsed)

    def interpret(self, parsed):
        """In case of security it's not allowed to call scripts recursively.
        """

        err = []
        warn = []
        if not parsed['处理文件']:
            err.append('未输入待处理文件\n')
            self.console.insert(END, "Error:" + err[-1])
            return
        else:
            files = parsed['处理文件']

            if len(files) is not 1:
                warn.append('输入多个文件excel/csv文件时, 请保证各个文件的字段名一致\n')
                self.console.insert(END, "Warning:" + warn[-1])
                old = pd.concat([
                    remove_undef_col(read_data(file_and_table))
                    for file_and_table in
                    map(lambda _: _.split('表名为'), files)])
            else:
                file = files[0]
                file_and_table = list(map(str.strip, file.split('表名为')))
                old = remove_undef_col(read_data(file_and_table))
            old.columns = old.columns.map(lambda _: _.replace('.', ''))

        old: pd.DataFrame
        new = pd.DataFrame(index=old.index)

        logics = list(Filter(parsed['选取']))
        selected = []

        for logic in [tuple(map(str.strip, logic.strip().split('='))) for logic in logics]:

            total = list(old.columns)
            total_arg_tps = ','.join(total)

            additional = True
            if len(logic) is 1:
                logic = logic * 2  # (name, )*2
                additional = False

            new_name, define = logic
            fn_get_new_field = eval(f' lambda {total_arg_tps}: ({define})')
            values = old.loc[:, total].values

            selected.append(new_name)
            new[new_name] = list(Map(values, fn_get_new_field))

            if additional:
                old[new_name] = new[new_name]

        new.columns = selected
        output_rule = parsed['输出位置']

        if len(output_rule) is 0:

            err.append('没有给出输出位置。\n')
            self.console.insert(END, "Error:" + err[-1])
            return

        elif len(output_rule) > 1:

            warn.append('只会取第一个输出位置生成规则。\n')
            self.console.insert(END, "Warning:" + warn[-1])

        output_rule = output_rule[0]

        total_arg_tps = list(new.columns)
        total_arg_tps_ = ','.join(total_arg_tps)
        fn_group = eval(f'lambda {total_arg_tps_}: ({output_rule})')

        sort_fn = None

        if parsed['排序依据']:
            sort_expr = "({})".format(','.join([f for f in Filter(parsed['排序依据'])]))
            sort_fn = eval(f'lambda {total_arg_tps_}: ({sort_expr})')

        for outfile, arrs in GroupBy(new.values, fn_group).items():

            if sort_fn:
                arrs = sorted(arrs, key=lambda _: sort_fn(*_))[::-1]

            write_date(
                pd.DataFrame(
                    arrs,
                    columns=total_arg_tps,
                    index=range(1, len(arrs) + 1)),
                filename=outfile)

            self.console.insert(END, f'写入{outfile}\n')

        self.console.insert(END, "操作成功。\n")

        # logging errors and warnings.
        for encoding in CodecList:
            try:
                with open(f'{self.log_path}/日志.txt', 'a+', encoding=encoding) as f:
                    if err:
                        f.write('Error(s):\t'  '\t\n'.join(err))
                    if warn:
                        f.write('Warnings(s):\t'  '\t\n'.join(warn))
                    break
            except UnicodeDecodeError:
                continue

    def display(self):
        """Fixed style
        """
        self.run_btn.grid(row=1, rowspan=1, column=0, columnspan=1, sticky=N + S + E + W, ipadx=50, pady=5)
        self.select_file_btn.grid(row=1, rowspan=1, column=2, columnspan=1, sticky=N + S + E + W, ipadx=50, pady=5)
        self.load_script.grid(row=1, rowspan=1, column=3, columnspan=1, sticky=N + S + E + W, ipadx=50, pady=5)
        self.editor.grid(row=3, rowspan=5, columnspan=10, column=0, sticky=N + S + E + W, pady=5)
        self.src_editor.grid(row=3, column=9, ipady=100)
        self.console.grid(row=3, rowspan=5, columnspan=5, column=10, sticky=N + S + E + W, pady=5)
        self.scr_console.grid(row=3, column=15, ipady=100)


if __name__ == '__main__':
    window = Manager()
    window.root.mainloop()
