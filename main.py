import streamlit as st
st.set_page_config(page_title="眼视光医学侦探", layout="wide")

# 页面跳转
def jump(page):
    st.session_state.page = page
    st.rerun()

# ========== 状态初始化 ==========
if "page" not in st.session_state:
    st.session_state.page = "start"

# 固定3次搜证次数
if "search_left" not in st.session_state:
    st.session_state.search_left = 3

# 五个地点独立开关（互不干扰，杜绝刷新BUG）
if "p1" not in st.session_state: st.session_state.p1 = False
if "p2" not in st.session_state: st.session_state.p2 = False
if "p3" not in st.session_state: st.session_state.p3 = False
if "p4" not in st.session_state: st.session_state.p4 = False
if "p5" not in st.session_state: st.session_state.p5 = False

# 答题完成状态
if "q1_done" not in st.session_state: st.session_state.q1_done = False
if "q2_done" not in st.session_state: st.session_state.q2_done = False
if "q3_done" not in st.session_state: st.session_state.q3_done = False

# 审问状态
if "ask_man" not in st.session_state: st.session_state.ask_man = ""
if "talk_txt" not in st.session_state: st.session_state.talk_txt = ""

# ========== 首页 完整原版背景 ==========
if st.session_state.page == "start":
    st.title("🔍 眼视光医学侦探 — 样本失窃解谜游戏")
    st.divider()
    st.subheader("📖 剧情背景")
    st.write("市中心医院眼视光样本库一份遗传性视网膜色素变性科研样本离奇失踪，")
    st.write("管理员无故昏迷，无外来闯入痕迹。")
    st.write("你作为特邀医学侦探，仅有3次搜证机会，谨慎选择探索地点！")
    st.divider()
    st.info("【此处后续插入：游戏封面图/动态视频】")
    if st.button("开始游戏", type="primary", use_container_width=True):
        jump("scene")

# ========== 案发现场 全文原样+无BUG次数逻辑 ==========
elif st.session_state.page == "scene":
    st.title("📍 案发现场 · 点击探索线索")
    st.info("【此处后续插入：案发现场全景背景图】")
    st.subheader(f"🔎 剩余搜证机会：{st.session_state.search_left} / 3")
    st.divider()

    # 次数为0 全部按钮禁用
    disable_all = st.session_state.search_left <= 0

    c1,c2,c3 = st.columns(3)
    c4,c5 = st.columns(2)

    # 1 冷藏柜旁
    with c1:
        if not st.session_state.p1:
            if st.button("1. 冷藏柜旁", disabled=disable_all):
                st.session_state.p1 = True
                st.session_state.search_left -= 1
                st.rerun()
        else:
            st.success("✅ 找到：破损视网膜相机存储卡")
            st.info("💡科普：眼底相机专门拍摄视网膜病变照片，存储卡需要加密存档，一旦破损容易造成患者眼底影像数据丢失。")
            st.text("🗣相关人员表述：这张存储卡并不是我日常使用的那一张。")
            if not st.session_state.q1_done:
                sel1 = st.radio("Q1：眼底相机存储卡必须满足什么要求？",
                    ["A. 普通SD卡容量越大越好","B. 必须加密专用卡保护隐私","C. 只用原厂卡无要求"],key="fix_q1")
                if st.button("提交答案1"):
                    if sel1 == "B. 必须加密专用卡保护隐私":
                        st.session_state.q1_done = True
                        st.success("答对！解锁关键线索：视频拍到张研究员案发前单独操作相机")
                    else:
                        st.error("答错了！正确答案是B")
            else:
                st.info("本题已作答完毕")

    # 2 实验台桌面
    with c2:
        if not st.session_state.p2:
            if st.button("2. 实验台桌面", disabled=disable_all):
                st.session_state.p2 = True
                st.session_state.search_left -= 1
                st.rerun()
        else:
            st.success("✅ 找到：视力与视野检测记录单")
            st.info("💡科普：遗传性视网膜色素变性人群，往往中心视力正常，但周边视野会逐渐缩小，只查裸眼视力很容易漏诊。")
            st.text("🗣相关人员表述：这份记录单是我平时整理的患者随访资料。")
            if not st.session_state.q2_done:
                sel2 = st.radio("Q2：视网膜色素变性典型视野特征？",
                    ["A. 中心暗点周边正常","B. 周边缩小、中心视力保留","C. 全视野下降"],key="fix_q2")
                if st.button("提交答案2"):
                    if sel2 == "B. 周边缩小、中心视力保留":
                        st.session_state.q2_done = True
                        st.success("答对！解锁关键线索：记录单笔迹为刘实习生")
                    else:
                        st.error("答错了！正确答案是B")
            else:
                st.info("本题已作答完毕")

    # 3 办公电脑屏幕
    with c3:
        if not st.session_state.p3:
            if st.button("3. 办公电脑屏幕", disabled=disable_all):
                st.session_state.p3 = True
                st.session_state.search_left -= 1
                st.rerun()
        else:
            st.success("✅ 找到：样本冷藏柜操作日志")
            st.info("💡科普：眼视光稀有病理样本需严格-20℃恒温冷藏，温度过低会破坏细胞活性，常温放置超过半小时即失效。")
            st.text("🗣相关人员表述：我近期很少登录样本库后台操作系统。")
            if not st.session_state.q3_done:
                sel3 = st.radio("Q3：眼视光样本标准保存温度？",
                    ["A. 4℃","B. -20℃","C. -80℃"],key="fix_q3")
                if st.button("提交答案3"):
                    if sel3 == "B. -20℃":
                        st.session_state.q3_done = True
                        st.success("答对！解锁关键线索：日志显示张研究员私自取出样本")
                    else:
                        st.error("答错了！正确答案是B")
            else:
                st.info("本题已作答完毕")

    # 4 资料书架
    with c4:
        if not st.session_state.p4:
            if st.button("4. 资料书架", disabled=disable_all):
                st.session_state.p4 = True
                st.session_state.search_left -= 1
                st.rerun()
        else:
            st.warning("🔍 仔细翻阅书架上专业书籍与档案资料，没有找到任何有用的线索，与本次样本失窃案关联不大。")

    # 5 门口走廊窗台
    with c5:
        if not st.session_state.p5:
            if st.button("5. 门口走廊窗台", disabled=disable_all):
                st.session_state.p5 = True
                st.session_state.search_left -= 1
                st.rerun()
        else:
            st.warning("🔍 仔细检查窗台、墙角与走廊角落，未发现可疑痕迹与遗留物品。")

    st.divider()
    if st.button("前往审问嫌疑人"):
        jump("sus_list")
    if st.button("返回首页"):
        jump("start")

# ========== 嫌疑人列表 原样不动 ==========
elif st.session_state.page == "sus_list":
    st.title("👥 审问室 · 选择嫌疑人")
    st.info("【此处后续插入：审问室背景图】")
    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1:
        st.info("【头像：张研究员】")
        if st.button("审问 张研究员"):
            st.session_state.ask_man = "张研究员"
            st.session_state.talk_txt = ""
            jump("ask_page")
    with c2:
        st.info("【头像：刘实习生】")
        if st.button("审问 刘实习生"):
            st.session_state.ask_man = "刘实习生"
            st.session_state.talk_txt = ""
            jump("ask_page")
    with c3:
        st.info("【头像：王技术员】")
        if st.button("审问 王技术员"):
            st.session_state.ask_man = "王技术员"
            st.session_state.talk_txt = ""
            jump("ask_page")
    st.divider()
    if st.button("前往最终指认"):
        jump("judge_page")
    if st.button("返回案发现场"):
        jump("scene")

# ========== 审问对话｜三人互相猜忌，动机均等无偏向 ==========
elif st.session_state.page == "ask_page":
    name = st.session_state.ask_man
    st.title(f"🔎 审问：{name}")
    st.divider()
    q_list = [
        "1. 眼底相机存储卡需要加密吗？",
        "2. 视网膜色素变性视野特点？",
        "3. 科研样本保存温度多少？",
        "4. 案发时间你在哪里？"
    ]
    if name == "张研究员":
        st.write("**潜在动机**：熟知样本库内部结构，日常出入自由，具备独立取走样本的条件")
        for q in q_list:
            if st.button(q):
                if q == q_list[0]:
                    st.session_state.talk_txt = "普通SD卡不用加密，患者信息不重要。"
                elif q == q_list[1]:
                    st.session_state.talk_txt = "视网膜色素变性是中心视力下降，周边视野没问题。"
                elif q == q_list[2]:
                    st.session_state.talk_txt = "科研样本必须保存在-80℃，-20℃根本存不住。"
                elif q == q_list[3]:
                    st.session_state.talk_txt = "案发时我不在样本库，我怀疑王技术员手握库房权限，有很大嫌疑私自拿取样本。"

    elif name == "刘实习生":
        st.write("**潜在动机**：常独自留守实验室，独处时间充足，行踪缺少旁人实时佐证")
        for q in q_list:
            if st.button(q):
                if q == q_list[0]:
                    st.session_state.talk_txt = "眼底影像属于患者隐私，存储卡必须加密。"
                elif q == q_list[1]:
                    st.session_state.talk_txt = "典型的视网膜色素变性是周边视野缩小，中心视力能长期保留。"
                elif q == q_list[2]:
                    st.session_state.talk_txt = "我记得老师说标准保存温度是-20℃，不是越低越好。"
                elif q == q_list[3]:
                    st.session_state.talk_txt = "案发时我确实在实验室，我觉得张研究员最近神色反常，同时也觉得王技术员行事十分可疑。"

    elif name == "王技术员":
        st.write("**潜在动机**：掌管库房门锁与温控设备，拥有不受限制进入存放区域的权限")
        for q in q_list:
            if st.button(q):
                if q == q_list[0]:
                    st.session_state.talk_txt = "医疗影像数据属于隐私，存储卡必须加密保护。"
                elif q == q_list[1]:
                    st.session_state.talk_txt = "视网膜色素变性的典型特征就是周边视野进行性缩小，这是眼视光的基础常识。"
                elif q == q_list[2]:
                    st.session_state.talk_txt = "我们样本库的标准保存温度就是-20℃，设备参数都是我调的，不会错。"
                elif q == q_list[3]:
                    st.session_state.talk_txt = "案发时我在检修设备，我既怀疑张研究员动机不纯，也觉得年轻实习生有贸然行动的可能。"

    if st.session_state.talk_txt:
        st.success(f"嫌疑人回答：{st.session_state.talk_txt}")
    st.divider()
    if st.button("返回嫌疑人列表"):
        jump("sus_list")

# ========== 最终指认页面｜三个按钮颜色完全一致 ==========
elif st.session_state.page == "judge_page":
    st.title("⚖️ 最终指认 · 锁定真凶")
    st.info("【此处后续插入：指认页背景视频/图片】")
    st.divider()
    st.write("结合线索和专业知识，选择你认定的真凶：")
    st.divider()
    if st.button("指认 张研究员"):
        jump("win_end")
    if st.button("指认 刘实习生"):
        jump("lose1_end")
    if st.button("指认 王技术员"):
        jump("lose2_end")
    st.divider()
    if st.button("返回审问室"):
        jump("sus_list")

# ========== 全部原版结局 ==========
elif st.session_state.page == "win_end":
    st.title("🎉 真相大白 · 案件侦破")
    st.info("【此处后续插入：成功结局视频】")
    st.write("你识破了张研究员的专业知识谎言！")
    st.write("他为掩盖科研数据造假，盗取稀有视网膜样本试图销毁证据，最终认罪落网。")
    st.divider()
    st.subheader("📚 眼视光科普总结")
    st.write("1. RP视网膜色素变性：周边视野缩小，中心视力长期正常")
    st.write("2. 眼视光样本标准保存温度：-20℃，非越低越好")
    st.write("3. 眼底影像存储卡必须加密，保护患者隐私")
    st.divider()
    if st.button("重新开始游戏"):
        st.session_state.clear()
        jump("start")

elif st.session_state.page == "lose1_end":
    st.title("❌ 推理错误 · 冤枉无辜")
    st.info("【此处后续插入：失败结局1视频】")
    st.write("你误指认勤恳的刘实习生，真凶张研究员连夜转移样本。")
    st.divider()
    st.subheader("📚 眼视光科普总结")
    st.write("1. RP周边视野先受损，仅查视力容易漏诊")
    st.write("2. 样本必须-20℃恒温冷藏")
    st.divider()
    if st.button("重新开始游戏"):
        st.session_state.clear()
        jump("start")

elif st.session_state.page == "lose2_end":
    st.title("❌ 推理错误 · 错怪好人")
    st.info("【此处后续插入：失败结局2视频】")
    st.write("王技术员仅负责设备维护，无作案动机。张研究员销毁证据后潜逃。")
    st.divider()
    st.subheader("📚 眼视光科普总结")
    st.write("对比嫌疑人专业知识回答，说谎者会违背基础眼视光常识。")
    st.divider()
    if st.button("重新开始游戏"):
        st.session_state.clear()
        jump("start")