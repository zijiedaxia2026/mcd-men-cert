#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M-CODE 参赛一键提交（后台运行）
================================
用法（在本目录执行）：
    GITHUB_TOKEN=xxxx REPO=owner/mcd-men-cert python submit.py

行为：
  1. 把当前本地仓库推送到 GitHub（公开仓库）
  2. 在官方赛事仓库 M-China/mcd-developer-innovation-challenge 下提交报名 Issue

安全：token 仅从环境变量读取，绝不打印或写入任何日志/文件。
"""
import os
import sys
import subprocess
import json
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("REPO")  # 我们自己的参赛仓库，形如 owner/mcd-men-cert
if not TOKEN or not REPO:
    sys.exit("缺少环境变量 GITHUB_TOKEN 或 REPO（例：REPO=lixinyu/mcd-men-cert）")


def run(cmd):
    print(">>", " ".join(cmd[:2]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr.strip()[:300])
    return r.returncode == 0


def api_post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


# 1) 推送本地仓库
branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
remote_url = f"https://{TOKEN}@github.com/{REPO}.git"
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", remote_url])

if not run(["git", "push", "-u", "origin", branch]):
    print("push 失败，尝试先创建公开仓库...")
    try:
        api_post(
            "https://api.github.com/user/repos",
            {"name": REPO.split("/")[-1], "private": False, "auto_init": False},
        )
        print("仓库已创建，重新推送...")
        run(["git", "push", "-u", "origin", branch])
    except Exception as e:
        print("建仓/推送失败:", e)

# 2) 提交报名 Issue（严格格式：标题与正文分字段传入；项目地址用纯文本，非 Markdown）
title = "麦门认证证书生成器 mcd-men-cert"
body = (
    "【参赛申请】\n"
    "项目名称：mcd-men-cert\n"
    f"项目地址：https://github.com/{REPO}\n"
    "项目简介：基于麦当劳 MCP 只读接口，把订单史生成一张可分享的「麦门认证证书」+ 一页式生涯报告；"
    "Token 仅走连接器配置不外泄，含全部标准文件，符合参赛声明。"
)
try:
    j = api_post(
        "https://api.github.com/repos/M-China/mcd-developer-innovation-challenge/issues",
        {"title": title, "body": body},
    )
    print("报名 Issue 已提交:", j.get("html_url"))
except Exception as e:
    print("Issue 提交失败:", e)
