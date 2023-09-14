import sys
import time
import tkinter as tk
from tkinter import scrolledtext

from pidReptile import *
from problemReptile import *

difficultyOptions = ["无选择", "暂无评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"]
fontStyle = ("微软雅黑", 24)
logFontStyle = ("微软雅黑", 17)


def invoke():
    # 获取条件 不输入时为 -1, [], ''
    difficulty = selectedDiff.get()
    tags = tagEntry.get().split(',')
    # 清除无效标签
    clearTags = [item for item in tags if item != '']
    keyword = keywordEntry.get()

    # 根据输入的条件爬取pid
    result1, result2 = getPids(difficulty, clearTags, keyword)
    if result1 == "invalid tag":
        print("请输入正确的标签！！")

    totalCount = result1
    problems = result2

    # 根据pid爬取题目
    cnt = 0
    for item in problems:
        pid = item["pid"]
        title = item["title"]
        result = getProblem(pid, title, difficulty, clearTags, keyword)
        if result == "error":
            print("爬取失败！")
            continue
        cnt += 1
        if cnt == 50:
            break


def redirect_output():
    # 输出日志
    def custom_write(msg):
        logText.insert(tk.END, msg)
        logText.see(tk.END)
        logText.update()

    # 将stdout和stderr重定向到自定义写函数
    sys.stdout.write = custom_write
    sys.stderr.write = custom_write


if __name__ == '__main__':
    # 创建主窗口
    window = tk.Tk()
    window.title("洛谷爬虫")
    window.geometry("600x400")
    window.configure(bg="#FFFFFF")

    # 设置题库
    typeLabel = tk.Label(window, text="题库:", font=fontStyle, bg="white", width=6)
    typeLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    luoguLabel = tk.Label(window, text="洛谷", font=fontStyle, bg="white", width=6)
    luoguLabel.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    # 设置难度下拉框
    difficultyFrame = tk.Frame(window, bg="white")
    difficultyFrame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
    diffLabel = tk.Label(difficultyFrame, text="难度:", font=fontStyle, bg="white", width=6)
    diffLabel.pack(side="left", padx=0, pady=10)
    selectedDiff = tk.StringVar(window, "无选择")
    diffMenu = tk.OptionMenu(difficultyFrame, selectedDiff, *difficultyOptions)
    diffMenu.config(width=18, height=1, font=fontStyle)
    diffMenu.pack(side="left", padx=10, pady=10)

    # 设置标签输入框
    tagFrame = tk.Frame(window, bg="white")
    tagFrame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
    tagLabel = tk.Label(tagFrame, text="标签:", font=fontStyle, bg="white", width=6)
    tagLabel.pack(side="left", padx=0, pady=10)
    tagEntry = tk.Entry(tagFrame, font=fontStyle, width=21, borderwidth=2, relief="solid")
    tagEntry.pack(side="left", padx=20, pady=10)

    # 设置关键词输入框
    keywordFrame = tk.Frame(window, bg="white")
    keywordFrame.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
    keywordLabel = tk.Label(keywordFrame, text="关键词:", font=fontStyle, bg="white", width=6)
    keywordLabel.pack(side="left", padx=0, pady=10)
    keywordEntry = tk.Entry(keywordFrame, font=fontStyle, width=21, borderwidth=2, relief="solid")
    keywordEntry.pack(side="left", padx=20, pady=10)

    # 设置启动按钮
    searchButton = tk.Button(window, text="爬取", font=fontStyle, width=8, height=1, command=invoke)
    searchButton.grid(row=4, column=1, padx=10, pady=10)

    # 设置日志
    logFrame = tk.Frame(window, bg="white")
    logFrame.grid(row=6, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

    logText = scrolledtext.ScrolledText(logFrame, font=logFontStyle, width=90, height=15, bg="#E0AB7F", relief="solid",
                                        bd=2)
    logText.pack()

    redirect_output()
    window.mainloop()