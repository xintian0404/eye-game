import streamlit as st
import subprocess
import sys
import webbrowser
import time

# 启动 Streamlit 的函数
def run_streamlit():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__, "--server.port=8501", "--server.headless=true"])
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

# 如果是被 Streamlit 运行，才执行游戏逻辑
if __name__ == "__main__":
    if not st.runtime.exists():
        run_streamlit()
    else:
        st.set_page_config(page_title="眼视光医学侦探", layout="wide")

        def jump(page):
            st.session_state.page = page
            st.rerun()

        # 初始化会话状态
        if "page" not in st.session_state:
            st.session_state.page = "start"
        if "search_left" not in st.session_state:
            st.session_state.search_left = 3
        if "p1" not in st.session_state: st.session_state.p1 = False
        if "p2" not in st.session_state: st.session_state.p2 = False
        if "p3" not in st.session_state: st.session_state.p3 = False
        if "p4" not in st.session_state: st.session_state.p4 = False
        if "p5" not in st.session_state: st.session_state.p5 = False
        if "q1_done" not in st.session_state: st.session_state.q1_done = False
        if "q2_done" not in st.session_state: st.session_state.q2_done = False
        if "q3_done" not in st.session_state: st.session_state.q3_done = False
        if "ask_man" not in st.session_state: st.session_state.ask_man = ""
        if "talk_txt" not in st.session_state: st.session_state.talk_txt = ""
        if "evidence1" not in st.session_state: st.session_state.evidence1 = False  # 商业合作单据
        if "evidence2" not in st.session_state: st.session_state.evidence2 = False  # 登录记录
        if "evidence3" not in st.session_state: st.session_state.evidence3 = False  # 资金记录
        if "evidence4" not in st.session_state: st.session_state.evidence4 = False  # 实习生加班记录
        if "evidence5" not in st.session_state: st.session_state.evidence5 = False  # 技术员检修记录

        # 首页
        if st.session_state.page == "start":
            st.title("🔍 眼视光医学侦探 — 样本失窃解谜游戏")
            st.divider()
            st.subheader("📖 剧情背景")
            st.write("市中心医院眼视光样本库，一份用于遗传性视网膜色素变性研究的关键样本离奇失踪。")
            st.write("管理员被发现时昏迷在值班室，身上无外伤，通风口残留微量吸入式麻醉剂痕迹。")
            st.write("样本库监控在案发当晚被短暂关闭，只有持有高级权限的人员才能操作。")
            st.write("你作为特邀医学侦探，仅有3次搜查机会，找出偷走样本的凶手，揭开样本背后的科研秘密！")
            st.divider()
            st.info("【此处可插入游戏封面图】")
            if st.button("开始游戏", type="primary", use_container_width=True):
                jump("scene")

        # 案发现场
        elif st.session_state.page == "scene":
            st.title("📍 案发现场 · 点击探索线索")
            st.info("【此处可插入案发现场全景图】")
            st.subheader(f"🔎 剩余搜查机会：{st.session_state.search_left} / 3")
            st.divider()
            disable_all = st.session_state.search_left <= 0

            c1, c2, c3 = st.columns(3)
            c4, c5 = st.columns(2)

            with c1:
                if not st.session_state.p1:
                    if st.button("1. 冷藏柜旁", disabled=disable_all):
                        st.session_state.p1 = True
                        st.session_state.search_left -= 1
                        st.session_state.evidence1 = True
                        st.rerun()
                else:
                    st.success("✅ 找到：破损眼底相机存储卡")
                    st.info("💡科普：眼底相机专门拍摄视网膜病变照片，存储卡需加密存档，破损易导致患者数据泄露。")
                    st.text("🗣相关人员表述：这张存储卡不是我日常使用的那一张。")
                    if st.session_state.evidence1:
                        st.warning("⚠️ 重要发现：存储卡缝隙中夹着一张商业实验合作单据碎片！")
                    if not st.session_state.q1_done:
                        sel1 = st.radio("Q1：眼底相机存储卡必须满足什么要求？",
                                        ["A. 普通SD卡容量越大越好", "B. 必须使用加密专用卡保护隐私", "C. 只要是原厂卡就行"], key="fix_q1")
                        if st.button("提交答案1"):
                            if sel1 == "B. 必须使用加密专用卡保护隐私":
                                st.session_state.q1_done = True
                                st.success("答对！解锁关键线索：相机最后一次使用记录显示操作人为管理员")
                            else:
                                st.error("答错了！正确答案是B，医疗数据需严格加密保护")
                    else:
                        st.info("本题已作答完毕")

            with c2:
                if not st.session_state.p2:
                    if st.button("2. 实验台桌面", disabled=disable_all):
                        st.session_state.p2 = True
                        st.session_state.search_left -= 1
                        st.session_state.evidence4 = True
                        st.rerun()
                else:
                    st.success("✅ 找到：视力与视野检查记录单")
                    st.info("💡科普：遗传性视网膜色素变性患者，早期表现为周边视野缩小，晚期发展为管状视野，中心视力通常正常。")
                    st.text("🗣相关人员表述：这份记录单不是我整理的患者随访资料。")
                    if st.session_state.evidence4:
                        st.warning("⚠️ 重要发现：记录单边缘有实习生的签名，但内容有明显修改痕迹！")
                    if not st.session_state.q2_done:
                        sel2 = st.radio("Q2：视网膜色素变性典型视野变化是？",
                                        ["A. 中心暗点周边正常", "B. 周边视野缩小，呈管状视野", "C. 全视野均匀缺损"], key="fix_q2")
                        if st.button("提交答案2"):
                            if sel2 == "B. 周边视野缩小，呈管状视野":
                                st.session_state.q2_done = True
                                st.success("答对！解锁关键线索：记录显示样本保存温度为-20℃")
                            else:
                                st.error("答错了！正确答案是B，这是该病的典型特征")
                    else:
                        st.info("本题已作答完毕")

            with c3:
                if not st.session_state.p3:
                    if st.button("3. 办公电脑屏幕", disabled=disable_all):
                        st.session_state.p3 = True
                        st.session_state.search_left -= 1
                        st.session_state.evidence2 = True
                        st.rerun()
                else:
                    st.success("✅ 找到：样本冷藏柜操作日志")
                    st.info("💡科普：眼视光生物样本短期保存温度为-20℃，长期保存需-80℃超低温，温度波动会导致样本失活。")
                    st.text("🗣相关人员表述：我近期很少登录样本库后台系统。")
                    if st.session_state.evidence2:
                        st.warning("⚠️ 重要发现：日志显示案发当晚有人登录系统，并修改了样本对外流转备案！")
                    if not st.session_state.q3_done:
                        sel3 = st.radio("Q3：眼视光科研样本的标准短期冷藏温度是？",
                                        ["A. 4℃冷藏", "B. -20℃恒温", "C. -80℃超低温"], key="fix_q3")
                        if st.button("提交答案3"):
                            if sel3 == "B. -20℃恒温":
                                st.session_state.q3_done = True
                                st.session_state.evidence3 = True
                                st.success("答对！解锁关键线索：医院近期有科研项目资金即将到期")
                            else:
                                st.error("答错了！正确答案是B，-20℃是这类样本的标准短期存储温度")
                    else:
                        st.info("本题已作答完毕")

            with c4:
                if not st.session_state.p4:
                    if st.button("4. 资料书架", disabled=disable_all):
                        st.session_state.p4 = True
                        st.session_state.search_left -= 1
                        st.session_state.evidence5 = True
                        st.rerun()
                else:
                    st.success("✅ 找到：设备维护记录")
                    st.info("💡科普：样本库的制冷和安防设备需要定期维护，确保样本保存环境稳定。")
                    st.text("🗣相关人员表述：我按照规定定期维护所有设备。")
                    if st.session_state.evidence5:
                        st.warning("⚠️ 重要发现：记录显示技术员案发前一周曾申请额外的麻醉剂用于设备调试！")

            with c5:
                if not st.session_state.p5:
                    if st.button("5. 门口走廊窗台", disabled=disable_all):
                        st.session_state.p5 = True
                        st.session_state.search_left -= 1
                        st.rerun()
                else:
                    st.success("✅ 找到：遗落的门禁卡")
                    st.info("💡科普：样本库门禁系统采用多级权限管理，不同人员拥有不同的访问权限。")
                    st.text("🗣相关人员表述：这不是我的门禁卡。")
                    st.warning("⚠️ 重要发现：门禁卡上有微弱的药物气味，但无法确定具体持有人")

            st.divider()
            if st.button("前往审问嫌疑人"):
                jump("sus_list")
            if st.button("返回首页"):
                jump("start")

        # 嫌疑人列表
        elif st.session_state.page == "sus_list":
            st.title("👥 审问室 · 选择嫌疑人")
            st.info("【此处可插入审问室背景图】")
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info("【头像：张研究员】")
                st.write("**资深项目负责人**")
                st.write("• 案发当晚曾登录样本库系统")
                st.write("• 项目即将结题，样本数据至关重要")
                st.write("• 对样本保存标准了如指掌")
                if st.button("审问 张研究员"):
                    st.session_state.ask_man = "张研究员"
                    st.session_state.talk_txt = ""
                    jump("ask_page")
            with c2:
                st.info("【头像：刘实习生】")
                st.write("**管理员助手**")
                st.write("• 案发当晚独自留在实验室加班")
                st.write("• 持有样本库基础权限")
                st.write("• 曾因操作失误被管理员批评")
                if st.button("审问 刘实习生"):
                    st.session_state.ask_man = "刘实习生"
                    st.session_state.talk_txt = ""
                    jump("ask_page")
            with c3:
                st.info("【头像：王技术员】")
                st.write("**设备维护员**")
                st.write("• 负责样本库设备维护")
                st.write("• 持有设备最高权限")
                st.write("• 熟悉所有安防和监控系统")
                if st.button("审问 王技术员"):
                    st.session_state.ask_man = "王技术员"
                    st.session_state.talk_txt = ""
                    jump("ask_page")
            st.divider()
            if st.button("前往最终指认"):
                jump("judge_page")
            if st.button("返回案发现场"):
                jump("scene")

        # 审讯页面
        elif st.session_state.page == "ask_page":
            name = st.session_state.ask_man
            st.title(f"🔎 审问：{name}")
            st.divider()

            # 展示当前收集到的证据
            st.subheader("📌 你目前掌握的证据：")
            if st.session_state.evidence1:
                st.info("✅ 存储卡中发现商业实验合作单据碎片")
            if st.session_state.evidence2:
                st.info("✅ 样本对外流转备案在案发当晚被修改")
            if st.session_state.evidence3:
                st.info("✅ 医院近期有科研项目资金即将到期")
            if st.session_state.evidence4:
                st.info("✅ 实习生签名的记录单有明显修改痕迹")
            if st.session_state.evidence5:
                st.info("✅ 技术员曾申请麻醉剂用于设备调试")
            if st.session_state.q1_done:
                st.info("✅ 相机最后一次使用记录显示操作人为管理员")
            if st.session_state.q2_done:
                st.info("✅ 样本库采用-20℃常规存储方式")

            st.divider()

            q_list = [
                "1. 案发当晚你在样本库做什么？",
                "2. 对于样本的保存温度，你有什么看法？",
                "3. 你对吸入式麻醉剂了解多少？",
                "4. 你觉得谁最有动机偷走样本？"
            ]

            if name == "张研究员":
                st.write("**人物特点：资深研究员，儒雅稳重，说话滴水不漏**")
                for q in q_list:
                    if st.button(q):
                        if q == q_list[0]:
                            st.session_state.talk_txt = "我只是例行核对样本存量，近期实验进度紧张，难免多上心。我对天发誓，绝对没有碰过样本！"

                        elif q == q_list[1]:
                            st.session_state.talk_txt = "这类珍贵样本自然稳妥至上，我一贯主张尽量长期超低温存放。-80℃虽然存取麻烦，但能最大限度保证样本活性。"

                        elif q == q_list[2]:
                            st.session_state.talk_txt = "我是做基础研究的，对临床麻醉药品不太了解。不过据我所知，只有熟悉医院药房的人才能拿到这类药剂。"

                        elif q == q_list[3]:
                            st.session_state.talk_txt = "依我看，刘实习生的嫌疑最大。他最近因工作失误被管理员严厉批评，案发当晚又独自留在实验室，而且他的记录单有明显修改痕迹，很可能是在掩盖什么。"


            elif name == "刘实习生":
                st.write("**人物特点：紧张胆怯，说话语无伦次，越解释越像心虚**")
                for q in q_list:
                    if st.button(q):
                        if q == q_list[0]:
                            st.session_state.talk_txt = "我在整理眼底病变筛查记录，管理员说我上次写错了，让我连夜改好。我真的没敢靠近样本柜！"

                        elif q == q_list[1]:
                            st.session_state.talk_txt = "平时入库大多放在零下二十度冰柜，长期封存才会转去超低温柜。这些基础流程我都记牢了。"

                        elif q == q_list[2]:
                            st.session_state.talk_txt = "我偶尔帮药房跑腿整理物资，见过但从来不敢私自触碰！我知道这是严重违规的！"

                        elif q == q_list[3]:
                            st.session_state.talk_txt = "我...我觉得王技术员有点可疑。他负责维护所有设备，有能力关闭监控系统，而且我听说他最近申请了麻醉剂，说是用于设备调试，但谁知道他真正想做什么..."


            elif name == "王技术员":
                st.write("**人物特点：沉默寡言，技术宅，对设备了如指掌**")
                for q in q_list:
                    if st.button(q):
                        if q == q_list[0]:
                            st.session_state.talk_txt = "上周刚检修过设备，一切正常。案发当晚我在家睡觉，有邻居可以作证。"

                        elif q == q_list[1]:
                            st.session_state.talk_txt = "超低温存取繁琐耗时，日常实验频繁取用，-20℃是兼顾活性与便利的最优选择。这是行业标准。"

                        elif q == q_list[2]:
                            st.session_state.talk_txt = "我负责维护通风系统，理论上知道如何投放。但安防管控严格，私自改动属于严重违纪。"

                        elif q == q_list[3]:
                            st.session_state.talk_txt = "张研究员的嫌疑最大。他的项目资金即将到期，急需样本数据完成论文，而且我发现他最近和校外机构有频繁联系，很可能是想把样本偷偷带出去牟利。"


            if st.session_state.talk_txt:
                st.success(f"嫌疑人回答：{st.session_state.talk_txt}")

            st.divider()
            if st.button("返回嫌疑人列表"):
                jump("sus_list")

        # 最终指认
        elif st.session_state.page == "judge_page":
            st.title("⚖️ 最终指认 · 锁定真凶")
            st.info("【此处可插入指认页面背景图】")
            st.divider()
            st.write("结合所有搜查线索和嫌疑人证词，你认为谁是偷走样本的凶手？")
            

            
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("指认 张研究员"):
                    jump("win_end")
            with col2:
                if st.button("指认 刘实习生"):
                    jump("lose1_end")
            with col3:
                if st.button("指认 王技术员"):
                    jump("lose2_end")
            
            st.divider()
            if st.button("返回审问室"):
                jump("sus_list")

        # 成功结局
        elif st.session_state.page == "win_end":
            st.title("🎉 真相大白 · 案件侦破")
            st.info("【此处可插入成功结局视频/图片】")
            st.write("你成功识破了张研究员的精心伪装！")
            st.write("他为了挽救即将失败的项目，利用职务便利修改了样本对外流转备案，准备将样本偷偷转移给校外合作方。")
            st.write("为了掩盖罪行，他故意强调-80℃存储的重要性，试图误导调查方向，同时栽赃给实习生和技术员。")
            st.divider()
            st.subheader("📚 眼视光科普总结")
            st.write("1. **视网膜色素变性**：遗传性眼病，早期表现为周边视野缩小，晚期发展为管状视野，目前尚无根治方法。")
            st.write("2. **样本保存标准**：眼视光生物样本短期保存温度为-20℃，长期保存需-80℃超低温，温度波动会导致样本失活。")
            st.write("3. **医疗安全管理**：医院的麻醉剂和样本库权限都有严格的管理制度，滥用权限和药品属于严重的违规行为。")
            st.write("4. **学术诚信**：科研工作必须坚持诚信原则，严禁私自将公共科研资源用于商业目的。")
            st.divider()
            if st.button("重新开始游戏"):
                st.session_state.clear()
                jump("start")

        # 失败结局1（误判实习生）
        elif st.session_state.page == "lose1_end":
            st.title("❌ 推理错误 · 冤枉无辜")
            st.info("【此处可插入失败结局视频/图片】")
            st.write("你错误地指认了勤恳工作的刘实习生！")
            st.write("这个年轻的实习生只是因为紧张和缺乏经验，才显得有些可疑。他根本没有接触核心样本的权限，也没有任何牟利动机。")
            st.write("真正的凶手张研究员趁机带着样本和校外合作方的资金远走高飞，再也无法追回。")
            st.divider()
            st.subheader("📚 案件反思")
            st.write("1. **不能仅凭言行判断**：紧张和胆怯不代表有罪，经验丰富的犯罪分子往往更加从容。")
            st.write("2. **重视客观证据**：权限记录、操作日志等客观证据比主观印象更可靠。")
            st.write("3. **动机分析要全面**：真正的犯罪往往伴随着明确的利益驱动，而不仅仅是情绪因素。")
            st.divider()
            if st.button("重新开始游戏"):
                st.session_state.clear()
                jump("start")

        # 失败结局2（误判技术员）
        elif st.session_state.page == "lose2_end":
            st.title("❌ 推理错误 · 错怪好人")
            st.info("【此处可插入失败结局视频/图片】")
            st.write("你错误地指认了技术精湛的王技术员！")
            st.write("这个沉默寡言的技术人员虽然拥有最高权限，但他只是一个热爱技术的纯粹工匠。他对设备的了解是为了更好地维护，而不是利用。")
            st.write("真正的凶手张研究员已经带着样本数据和商业合作的收益消失得无影无踪。")
            st.divider()
            st.subheader("📚 案件反思")
            st.write("1. **权力不等于动机**：拥有作案条件不代表就有作案意愿。")
            st.write("2. **专业不等于犯罪**：对专业领域的精通是工作所需，不应因此受到怀疑。")
            st.write("3. **不要被表面现象迷惑**：最明显的嫌疑人往往是被精心设计的替罪羊。")
            st.divider()
            if st.button("重新开始游戏"):
                st.session_state.clear()
                jump("start")