"""
========================================================
           通用“刷课 + 进度提交”示例脚本（占位符版）
========================================================

 • 仅演示思路；所有   TODO_xxx  字段请读者根据目标站点自行补充。
 • 请确保行为符合目标网站的《用户协议》及〈机器人抓取策略〉。
 • 若出现任何法律/合规问题，务必停止使用并寻求专业意见。
"""

import csv, re, time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import ddddocr

# ================== 基本配置（全部需自行替换） ==================
BASE_DOMAIN   = "TODO_your_domain.com"        # 目标根域
COURSE_CID    = "TODO_project_id"             # 项目/课程 ID
CSV_PATH      = "credentials.csv"             # 用户名、密码 CSV
CAPTCHA_LEN   = 5                             # 图形验证码位数
HEADLESS      = False                         # True=无界面
# ===============================================================

ocr = ddddocr.DdddOcr(show_ad=False)
start_times = {}                       # 记录各课件最后提交

# ---------- 读取账号 ----------
def read_credentials(path):
    with open(path, encoding="utf-8-sig") as f:
        return [(r["username"], r["password"])
                for r in csv.DictReader(f)
                if r.get("username") and r.get("password")]

# ---------- 登录 ----------
def playwright_login(username, password, p):
    """Playwright 自动登录，返回 (top_domain, requests.Session)"""
    browser = p.chromium.launch(headless=HEADLESS)
    page    = browser.new_page()
    sess    = requests.Session()

    # (1) 进入登录页
    page.goto(f"https://{BASE_DOMAIN}/TODO_LOGIN_PATH", wait_until="networkidle")

    # (2) 若需点击“密码登录”之类按钮，请自行补充
    # page.click("TODO_SELECTOR_show_pwd")

    while "login" in page.url.lower():
        try:
            page.fill("TODO_selector_username", username)
            page.fill("TODO_selector_pwd_box",  password)
            page.evaluate("pwd => document.querySelector('TODO_hidden_pwd').value = pwd", password)

            # 捕获验证码
            img_bytes = page.query_selector("TODO_selector_captcha_img").screenshot()
            code_raw  = ocr.classification(img_bytes)
            code      = "".join(re.findall(r"\d", code_raw))

            if len(code) != CAPTCHA_LEN:
                page.query_selector("TODO_selector_captcha_img").click()
                time.sleep(1)
                continue

            page.fill("TODO_selector_captcha_input", code)
            page.check("TODO_selector_agree_checkbox")
            page.click("TODO_selector_login_button")
            page.wait_for_load_state()
        except Exception as e:
            print("[login] error:", e)
            time.sleep(1)

        if "login" not in page.url.lower():
            break

    # 同步 cookie
    for c in page.context.cookies():
        sess.cookies.set(c["name"], c["value"], domain=c["domain"])

    browser.close()
    print(f"[{username}] 登录成功")
    return sess

# ---------- 获取课件 CWID ----------
def fetch_cwids(sess):
    html = sess.get(f"https://{BASE_DOMAIN}/TODO_course_page?cid={COURSE_CID}").text
    pattern = re.compile(r"course_ware\.aspx\?cwid=([0-9a-fA-F-]{36})", re.I)
    cwids = list(set(pattern.findall(html)))
    print("CWID 列表:", cwids)
    return cwids

# ---------- 判断课程/项目是否已完成 ----------
def is_course_finished(sess, cwid):
    url  = f"https://{BASE_DOMAIN}/TODO_exam_result?cwid={cwid}"
    html = sess.get(url, timeout=10).text
    cond = ("TODO_课件完毕关键字" in html and
            "TODO_项目完毕关键字" in html and
            "TODO_立即学习关键字" not in html)
    if cond:
        print(f"[{cwid}] 已满足项目完成条件")
    return cond

# ---------- 后台接口 ----------
def update_process(sess, params, status):
    params["status"] = status
    url = f"https://{BASE_DOMAIN}/TODO_update_endpoint"
    sess.get(url, params=params)

def add_play_record(sess, params):
    url = f"https://{BASE_DOMAIN}/TODO_record_endpoint"
    data = {k: params[k] for k in ("relation_id", "course_id", "user_id")}
    sess.get(url, params=data)

# ---------- 主刷课逻辑 ----------
def learn_course(username, password, p):
    sess  = playwright_login(username, password, p)
    cwids = fetch_cwids(sess)

    done_flag = {c: False for c in cwids}
    for c in cwids:
        if is_course_finished(sess, c):      # 快速跳过已完成
            done_flag[c] = True

    counter = {c: 0 for c in cwids}

    while True:
        pending = [c for c, done in done_flag.items() if not done]
        if not pending:
            print(f"[{username}] 全部课件已完成")
            return

        for cwid in pending:
            if is_course_finished(sess, cwid):   # 项目整体完成 → 直接返回
                return

            # 5min 速率限制
            gap = 302 - (datetime.now() - start_times.get(cwid, datetime.now() - timedelta(seconds=302))).total_seconds()
            if gap > 0: time.sleep(gap)

            html = sess.get(f"https://{BASE_DOMAIN}/TODO_courseware_page?cwid={cwid}").text
            # ↓ 根据页面提取真实参数键名 ↓
            params = {
                "group_id":  re.search(r"group_id:'(.+?)'",  html).group(1),
                "relation_id":re.search(r"cwrid:'(.+?)'",    html).group(1),
                "user_id":   re.search(r"uid:'(.+?)'",       html).group(1),
                "course_id": COURSE_CID,
                # 其余字段……
            }

            # 交替提交 1 & 2
            if counter[cwid] < 5:
                update_process(sess, params, 1);  counter[cwid] += 1
            else:
                update_process(sess, params, 2);  counter[cwid]  = 0

            add_play_record(sess, params)
            start_times[cwid] = datetime.now()

            done_flag[cwid] = "TODO_在线考试关键字" in sess.get(
                f"https://{BASE_DOMAIN}/TODO_exam_page?cwid={cwid}"
            ).text

# ---------- 入口 ----------
def main():
    creds = read_credentials(CSV_PATH)
    print("账号数量:", len(creds))

    with sync_playwright() as p:
        with ThreadPoolExecutor(max_workers=len(creds)) as pool:
            futs = [pool.submit(learn_course, u, pw, p)
                    for u, pw in creds]
            for f in futs: f.result()

if __name__ == "__main__":
    main()
