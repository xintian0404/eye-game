import streamlit as st
import base64
from PIL import Image
import time

st.set_page_config(page_title="眼视光医学侦探", layout="wide")

# ====================== 工具函数 ======================
@st.cache_data
def img_to_base64(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def load_img(path, width=None):
    try:
        im = Image.open(path)
        if width:
            h = int(im.height * width / im.width)
            im = im.resize((width, h))
        return im
    except:
        return Image.new("RGB", (300, 200), "#1a1a1a")

def load_vid(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except:
        return None

def load_audio(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except:
        return None

def jump(page):
    st.session_state.page = page
    st.session_state.vid_finish = False
    st.rerun()

# ====================== 资源路径 ======================
BG = {
    "cover": "images/01_游戏封面图.jpg",
    "scene": "images/02_案发现场全景.jpg",
    "ask": "images/11_审问室背景.jpg",
    "judge": "images/12_指认页背景.jpg",
}

AUDIO = {
    "start": "audios/bgm_start.m4a",
    "scene": "audios/bgm_scene.m4a",
    "ask": "audios/bgm_ask.m4a",
    "judge": "audios/bgm_judge.m4a",
    "end": "audios/bgm_end.m4a",
}

IMG = {
    "clue1": "images/03_线索1_破损存储卡特写.jpg",
    "clue2": "images/04_线索2_视野检测单.jpg",
    "clue3": "images/05_线索3_电脑操作日志.jpg",
    "clue4": "images/06_无效线索_书架.jpg",
    "clue5": "images/07_无效线索_窗台.jpg",
    "zhang": "images/08_张研究员头像.jpg",
    "liu": "images/09_刘实习生头像.jpg",
    "wang": "images/10_王技术员头像.jpg",
}

VIDEO = {
    "cover": "videos/01_封面视频.mp4",
    "scene": "videos/02_案发现场视频.mp4",
    "judge": "videos/03_指认页视频.mp4",
    "win": "videos/04_成功结局.mp4",
    "lose_liu": "videos/05_失败结局_刘实习生.mp4",
    "lose_wang": "videos/06_失败结局_王技术员.mp4",
}

# ====================== 初始化 ======================
if "page" not in st.session_state:
    st.session_state.page = "start"
if "vid_finish" not in st.session_state:
    st.session_state.vid_finish = False
if "last_bgm" not in st.session_state:
    st.session_state.last_bgm = ""

init_keys = ["search_left","p1","p2","p3","p4","p5","ask_man","talk_txt","evidence1","evidence2","evidence3","evidence4","evidence5"]
init_vals = [3,False,False,False,False,False,"","",False,False,False,False,False]
for k,v in zip(init_keys, init_vals):
    if k not in st.session_state:
        st.session_state[k] = v

if "evidence_list" not in st.session_state:
    st.session_state.evidence_list = []
if "leak_analysis" not in st.session_state:
    st.session_state.leak_analysis = ""
if "show_ai_check" not in st.session_state:
    st.session_state.show_ai_check = False
if "q1_ok" not in st.session_state: st.session_state.q1_ok = False
if "q2_ok" not in st.session_state: st.session_state.q2_ok = False
if "q3_ok" not in st.session_state: st.session_state.q3_ok = False
if "q4_ok" not in st.session_state: st.session_state.q4_ok = False
if "q5_ok" not in st.session_state: st.session_state.q5_ok = False

# ====================== 终极修复：彻底删除所有黑框、边框、阴影、轮廓 ======================
st.markdown("""
<style>
/* 全局清除所有边框和黑框 */
* {
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

html, body {
    height: 100vh !important;
    overflow: auto !important;
    background: transparent !important;
}

/* 页面容器彻底无框 */
.stApp {
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

.block-container {
    position: relative !important;
    z-index: 99 !important;
    padding: 1rem 2rem !important;
    max-width: 100% !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* 卡片彻底透明无框 */
.suspense-card {
    background: transparent !important;
    padding: 10px 0 !important;
    margin: 8px 0 !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    border-radius: 0 !important;
}

/* 文字颜色保留 */
h1,h2,h3,p,div,span {
    color: white !important;
}
.red-text{color:#ff4444 !important; font-weight:bold;}
.green-text{color:#79ff79 !important; font-weight:bold;}
.blue-text{color:#66ccff !important; font-weight:bold;}
.yellow-text{color:#ffdd66 !important; font-weight:bold;}

/* 按钮样式保留 */
.stButton>button{
    background:linear-gradient(135deg,#b71c1c,#d32f2f) !important;
    color:white !important;
    font-weight:bold !important;
    border-radius:10px !important;
    padding:12px !important;
    border: none !important;
    box-shadow: none !important;
}

/* 图片无框无阴影 */
img{
    border-radius:12px !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* 隐藏页脚、音频组件 */
footer{visibility:hidden !important;}
div[data-testid="stAudio"]{display:none !important; height:0 !important; opacity:0 !important;}

/* Streamlit自带组件全部去框 */
div[data-testid="stMarkdownContainer"],
div[data-testid="stExpander"],
div[data-testid="stImage"],
div[data-testid="stButton"] {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}

/* 结局文字黑色 */
.end-text * {
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

# ====================== 5场景自动切换BGM（隐藏播放） ======================
def play_bgm_by_page():
    page_map = {
        "start": "start",
        "scene": "scene",
        "sus_list": "ask",
        "ask_page": "ask",
        "judge_page": "judge",
        "win_end": "end",
        "lose1_end": "end",
        "lose2_end": "end"
    }
    key = page_map.get(st.session_state.page, "")
    if not key or key == st.session_state.last_bgm:
        return
    st.session_state.last_bgm = key
    audio = load_audio(AUDIO[key])
    if audio:
        st.audio(audio, format="audio/m4a", loop=True, autoplay=True)

play_bgm_by_page()

# ====================== AI核心函数 ======================
def ai_classify_evidence(ev_list):
    classify_dict = {"物证":[],"书证":[],"辅助线索":[]}
    for item in ev_list:
        if "存储卡" in item or "门禁卡" in item:
            classify_dict["物证"].append(item)
        elif "记录单" in item or "操作日志" in item:
            classify_dict["书证"].append(item)
        else:
            classify_dict["辅助线索"].append(item)
    return classify_dict

def ai_check_confession_leak(name, answer, ev_list):
    leak = ""
    all_evi = str(ev_list)
    if name == "张研究员":
        if "-80℃保存" in answer and "修改日志" in all_evi:
            leak += "【漏洞2】明知标本必须超低温存放，却在案发当晚私自篡改样本备案记录，刻意隐瞒当晚进入冷库事实；\n"
        if "没进储藏室" in answer and "门禁卡" in all_evi:
            leak += "【漏洞3】现场遗留最高权限门禁卡只有研究员持有，说谎未曾进入库房明显撒谎；"
    elif name == "刘实习生":
        if "没修改单据" in answer and "修改签名" in all_evi:
            leak += "【漏洞1】笔录否认修改实验记录，但是留存单据留有本人修改笔迹；\n"
        if "八点离开" in answer and "夜班登记" in all_evi:
            leak += "【漏洞2】答对科普解锁隐藏线索：夜班登记显示他深夜十点仍滞留院内，离开时间说谎；"
    elif name == "王技术员":
        if "居家休息" in answer and "申领麻醉剂" in all_evi:
            leak += "【漏洞1】事前申领麻醉药物，却声称案发全天在家无外出，无法提供不在场客观凭证；\n"
        if "只管设备" in answer and "通风管控" in all_evi:
            leak += "【漏洞2】隐藏线索：通风管路只有他能全开，谎称不懂麻醉投放条件刻意避重就轻；"
    if leak == "":
        leak = "当前口供与已搜集证据暂无明显矛盾，未发现逻辑漏洞。"
    return leak

# ====================== 页面内容 ======================
# 1封面
if st.session_state.page == "start":
    if not st.session_state.vid_finish:
        v = load_vid(VIDEO["cover"])
        if v:
            st.video(v, autoplay=True, muted=True, loop=False)
            time.sleep(5)
            st.session_state.vid_finish = True
            st.rerun()
    else:
        bg = img_to_base64(BG["cover"])
        st.markdown(f'<style>.stApp{{background-image:url("data:image/jpg;base64,{bg}");}}</style>', unsafe_allow_html=True)
        st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
        st.title("🔍 眼视光医学侦探 — 样本失窃解谜游戏")
        st.markdown("""
市中心医院眼视光样本库，一份用于<span class='red-text'>遗传性视网膜色素变性</span>研究的关键样本离奇失踪。

管理员被发现时昏迷在值班室，身上无外伤，通风口残留微量<span class='red-text'>吸入式麻醉剂</span>痕迹。

样本库监控在案发当晚被短暂关闭，只有持有<span class='red-text'>高级权限</span>的人员才能操作。

你作为特邀医学侦探，仅有<span class='red-text'>3次搜查机会</span>，找出偷走样本的凶手，揭开样本背后的科研秘密！
""", unsafe_allow_html=True)
        if st.button("开始游戏", use_container_width=True):
            jump("scene")
        st.markdown('</div>', unsafe_allow_html=True)

# 2案发现场
elif st.session_state.page == "scene":
    if not st.session_state.vid_finish:
        v = load_vid(VIDEO["scene"])
        if v:
            st.video(v, autoplay=True, muted=True, loop=False)
            time.sleep(5)
            st.session_state.vid_finish = True
            st.rerun()
    else:
        bg = img_to_base64(BG["scene"])
        st.markdown(f'<style>.stApp{{background-image:url("data:image/jpg;base64,{bg}");}}</style>', unsafe_allow_html=True)
        st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
        st.title("📍 案发现场 · 点击探索线索")
        st.markdown(f"🔎 剩余搜查机会：<span class='red-text'>{st.session_state.search_left}/3</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        disable = st.session_state.search_left <= 0
        c1,c2,c3 = st.columns(3)
        c4,c5 = st.columns(2)

        #线索1
        with c1:
            st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
            if not st.session_state.p1:
                if st.button("1.冷藏柜旁", disabled=disable):
                    st.session_state.p1=True
                    st.session_state.search_left-=1
                    st.session_state.evidence1=True
                    if "破损眼底相机存储卡、商业合作单据碎片" not in st.session_state.evidence_list:
                        st.session_state.evidence_list.append("破损眼底相机存储卡、商业合作单据碎片")
                    st.rerun()
            else:
                st.success("✅找到：破损眼底相机存储卡")
                st.image(load_img(IMG["clue1"],300), width=300)
                st.markdown("⚠️重要发现：存储卡缝隙中夹着商业实验合作单据碎片！", unsafe_allow_html=True)
                with st.expander("💡眼科科普单选答题（答对解锁隐藏线索）"):
                    st.markdown("Q：遗传性视网膜色素变性（RP）最早典型临床表现？")
                    b1,b2,b3 = st.columns(3)
                    with b1:
                        if st.button("A.突发中心视力骤升",key="q1_a") and not st.session_state.q1_ok:
                            st.warning("回答错误，无额外线索")
                    with b2:
                        if st.button("B.自幼夜盲+周边视野渐进性缺损",key="q1_b") and not st.session_state.q1_ok:
                            st.session_state.q1_ok=True
                            st.session_state.evidence_list.append("隐藏线索1：单据备注药企预付款，研究员私下对接商业项目")
                            st.success("答对！获得隐藏关键线索已自动存入证据库！")
                    with b3:
                        if st.button("C.固定眼前黑影",key="q1_c") and not st.session_state.q1_ok:
                            st.warning("回答错误，无额外线索")
            st.markdown('</div>', unsafe_allow_html=True)

        #线索2
        with c2:
            st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
            if not st.session_state.p2:
                if st.button("2.实验台桌面", disabled=disable):
                    st.session_state.p2=True
                    st.session_state.search_left-=1
                    st.session_state.evidence4=True
                    if "视野检查记录单（存在修改签名）" not in st.session_state.evidence_list:
                        st.session_state.evidence_list.append("视野检查记录单（存在修改签名）")
                    st.rerun()
            else:
                st.success("✅找到：视力与视野检查记录单")
                st.image(load_img(IMG["clue2"],300), width=300)
                st.markdown("⚠️重要发现：记录单边缘有实习生签名，内容存在修改痕迹！", unsafe_allow_html=True)
                with st.expander("💡眼科科普单选答题（答对解锁隐藏线索）"):
                    st.markdown("Q：临床自动视野计首要适用目的？")
                    b1,b2,b3 = st.columns(3)
                    with b1:
                        if st.button("A.单纯验光配镜",key="q2_a") and not st.session_state.q2_ok:
                            st.warning("回答错误，无额外线索")
                    with b2:
                        if st.button("B.筛查青光眼、视神经及视网膜器质性病变",key="q2_b") and not st.session_state.q2_ok:
                            st.session_state.q2_ok=True
                            st.session_state.evidence_list.append("隐藏线索2：夜班签到表，实习生案发深夜十点仍滞留院内")
                            st.success("答对！获得隐藏关键线索已自动存入证据库！")
                    with b3:
                        if st.button("C.确诊干眼症",key="q2_c") and not st.session_state.q2_ok:
                            st.warning("回答错误，无额外线索")
            st.markdown('</div>', unsafe_allow_html=True)

        #线索3
        with c3:
            st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
            if not st.session_state.p3:
                if st.button("3.办公电脑屏幕", disabled=disable):
                    st.session_state.p3=True
                    st.session_state.search_left-=1
                    st.session_state.evidence2=True
                    if "样本冷藏柜操作日志（案发备案被篡改）" not in st.session_state.evidence_list:
                        st.session_state.evidence_list.append("样本冷藏柜操作日志（案发备案被篡改）")
                    st.rerun()
            else:
                st.success("✅找到：样本冷藏柜操作日志")
                st.image(load_img(IMG["clue3"],300), width=300)
                st.markdown("⚠️重要发现：案发当晚有人修改样本流转备案！", unsafe_allow_html=True)
                with st.expander("💡眼科科普单选答题（答对解锁隐藏线索）"):
                    st.markdown("Q：人眼视网膜病理标本超低温冷冻保存核心目的？")
                    b1,b2,b3 = st.columns(3)
                    with b1:
                        if st.button("A.防虫防潮",key="q3_a") and not st.session_state.q3_ok:
                            st.warning("回答错误，无额外线索")
                    with b2:
                        if st.button("B.维持组织细胞活性，用于遗传性眼病病理与新药研发",key="q3_b") and not st.session_state.q3_ok:
                            st.session_state.q3_ok=True
                            st.session_state.evidence_list.append("隐藏线索3：日志权限只有张研究员拥有修改审批权限")
                            st.success("答对！获得隐藏关键线索已自动存入证据库！")
                    with b3:
                        if st.button("C.降低储存占地",key="q3_c") and not st.session_state.q3_ok:
                            st.warning("回答错误，无额外线索")
            st.markdown('</div>', unsafe_allow_html=True)

        #线索4
        with c4:
            st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
            if not st.session_state.p4:
                if st.button("4.资料书架", disabled=disable):
                    st.session_state.p4=True
                    st.session_state.search_left-=1
                    st.session_state.evidence5=True
                    if "设备维护记录：技术员申领麻醉剂" not in st.session_state.evidence_list:
                        st.session_state.evidence_list.append("设备维护记录：技术员申领麻醉剂")
                    st.rerun()
            else:
                st.success("✅找到：设备维护记录")
                st.image(load_img(IMG["clue4"],300), width=300)
                st.markdown("⚠️重要发现：技术员案发前申领额外麻醉剂！", unsafe_allow_html=True)
                with st.expander("💡眼科科普单选答题（答对解锁隐藏线索）"):
                    st.markdown("Q：眼科临床吸入式全身麻醉主要适用场景？")
                    b1,b2,b3 = st.columns(3)
                    with b1:
                        if st.button("A.框架眼镜验配",key="q4_a") and not st.session_state.q4_ok:
                            st.warning("回答错误，无额外线索")
                    with b2:
                        if st.button("B.低龄儿童复杂眼底/玻璃体手术",key="q4_b") and not st.session_state.q4_ok:
                            st.session_state.q4_ok=True
                            st.session_state.evidence_list.append("隐藏线索4：通风总阀由设备技术员单人管控开闭")
                            st.success("答对！获得隐藏关键线索已自动存入证据库！")
                    with b3:
                        if st.button("C.干眼理疗",key="q4_c") and not st.session_state.q4_ok:
                            st.warning("回答错误，无额外线索")
            st.markdown('</div>', unsafe_allow_html=True)

        #线索5
        with c5:
            st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
            if not st.session_state.p5:
                if st.button("5.门口走廊窗台", disabled=disable):
                    st.session_state.p5=True
                    st.session_state.search_left-=1
                    if "现场遗留陌生门禁卡" not in st.session_state.evidence_list:
                        st.session_state.evidence_list.append("现场遗留陌生门禁卡")
                    st.rerun()
            else:
                st.success("✅找到：遗落门禁卡")
                st.image(load_img(IMG["clue5"],300), width=300)
                with st.expander("💡管理常识单选答题（答对解锁隐藏线索）"):
                    st.markdown("Q：科研标本库房最高等级审批门禁权限归属？")
                    b1,b2,b3 = st.columns(3)
                    with b1:
                        if st.button("A.轮转实习人员",key="q5_a") and not st.session_state.q5_ok:
                            st.warning("回答错误，无额外线索")
                    with b2:
                        if st.button("B.设备维修技术员",key="q5_b") and not st.session_state.q5_ok:
                            st.warning("回答错误，无额外线索")
                    with b3:
                        if st.button("C.在研项目负责人（研究员）",key="q5_c") and not st.session_state.q5_ok:
                            st.session_state.q5_ok=True
                            st.session_state.evidence_list.append("隐藏线索5：遗失门禁卡为张研究员专属权限卡")
                            st.success("答对！获得隐藏关键线索已自动存入证据库！")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="suspense-card">',unsafe_allow_html=True)
        st.markdown("<span class='green-text'>【自动实时汇总：当前全部已搜集证据清单】</span>",unsafe_allow_html=True)
        if len(st.session_state.evidence_list)==0:
            st.markdown("暂无搜集到任何线索")
        else:
            for idx,item in enumerate(st.session_state.evidence_list,1):
                st.markdown(f"{idx}.{item}")
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="suspense-card">',unsafe_allow_html=True)
        if st.button("🔍AI汇总全部已收集证据并智能分类",use_container_width=True):
            classify_res = ai_classify_evidence(st.session_state.evidence_list)
            txt = f"""<span class='green-text'>【AI全证据汇总分类结果】</span>
<b>物证：</b>{classify_res['物证']}
<b>书证：</b>{classify_res['书证']}
<b>辅助线索：</b>{classify_res['辅助线索']}"""
            st.markdown(txt,unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

        col1,col2=st.columns(2)
        with col1:
            if st.button("前往审问嫌疑人",use_container_width=True):
                jump("sus_list")
        with col2:
            if st.button("返回首页",use_container_width=True):
                jump("start")

#3嫌疑人选择页
elif st.session_state.page == "sus_list":
    bg = img_to_base64(BG["ask"])
    st.markdown(f'<style>.stApp{{background-image:url("data:image/jpg;base64,{bg}");}}</style>', unsafe_allow_html=True)
    st.title("👥审问室 · 选择嫌疑人")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
        st.image(load_img(IMG["zhang"],200), width=200, caption="张研究员")
        if st.button("审问张研究员", use_container_width=True):
            st.session_state.ask_man="张研究员"
            st.session_state.talk_txt = ""
            st.session_state.leak_analysis = ""
            st.session_state.show_ai_check = False
            jump("ask_page")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
        st.image(load_img(IMG["liu"],200), width=200, caption="刘实习生")
        if st.button("审问刘实习生", use_container_width=True):
            st.session_state.ask_man="刘实习生"
            st.session_state.talk_txt = ""
            st.session_state.leak_analysis = ""
            st.session_state.show_ai_check = False
            jump("ask_page")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
        st.image(load_img(IMG["wang"],200), width=200, caption="王技术员")
        if st.button("审问王技术员", use_container_width=True):
            st.session_state.ask_man="王技术员"
            st.session_state.talk_txt = ""
            st.session_state.leak_analysis = ""
            st.session_state.show_ai_check = False
            jump("ask_page")
        st.markdown('</div>', unsafe_allow_html=True)
    col_a,col_b = st.columns(2)
    with col_a:
        if st.button("最终指认凶手", use_container_width=True):
            jump("judge_page")
    with col_b:
        if st.button("返回案发现场", use_container_width=True):
            jump("scene")

#4单人审问
elif st.session_state.page == "ask_page":
    bg = img_to_base64(BG["ask"])
    st.markdown(f'<style>.stApp{{background-image:url("data:image/jpg;base64,{bg}");}}</style>', unsafe_allow_html=True)
    name = st.session_state.ask_man
    st.title(f"🔎 审问：{name}")
    qlist=["1.案发当晚你在样本库做什么？","2.你对样本保存温度怎么看？","3.了解吸入式麻醉剂吗？","4.你认为谁嫌疑最大？"]
    st.markdown('<div class="suspense-card">', unsafe_allow_html=True)
    for q in qlist:
        if st.button(q):
            if name=="张研究员":
                ans={
                "1.案发当晚你在样本库做什么？":"我整晚都在办公室核对全年实验库存清单，中途没有进入标本储藏室，失窃样本不在我的经手台账里，下班前检查门窗全部落锁。",
                "2.你对样本保存温度怎么看？":"这类珍贵病理样本长期科研保存必须稳定-80℃超低温冷藏，短期周转才会临时放置在零下二十度冰箱，院内实验规范白纸黑字写得很明确。",
                "3.了解吸入式麻醉剂吗？":"麻醉药品统一由药房专人管控申领，我是科研研究员，不参与临床用药调配，从来没有申领、接触任何吸入麻醉药剂的权限。",
                "4.你认为谁嫌疑最大？":"刘实习生日常做事马虎粗心，多次修改实验记录被我批评，案发前还来过库房抄写数据，大概率是他私自操作偷走样本。"}[q]
            elif name=="刘实习生":
                ans={
                "1.案发当晚你在样本库做什么？":"当天临近实习考核，我留在实验区抄写实习总结与检查记录，全程只在操作台活动，没有靠近深处样本储藏冷库，晚上八点左右就正常离开院区。",
                "2.你对样本保存温度怎么看？":"课堂上学过，短期实验用标本常规-20℃保存，需要长期留存做课题的标本统一转入超低温冰箱，我只是实习人员没有冷库开门权限。",
                "3.了解吸入式麻醉剂吗？":"偶尔跟着带教老师去药房取药，只负责跑腿递送，药剂领用登记需要医师签字审批，我没有资格私自领取任何麻醉类药物。",
                "4.你认为谁嫌疑最大？":"王技术员掌管全库房设备与监控系统，能随意关停监控设备，还能进出冷库检修设备，他具备独自动手作案的条件。"}[q]
            else:
                ans={
                "1.案发当晚你在样本库做什么？":"白天完成全院区制冷设备巡检，傍晚下班回家休息，整晚居家，没有再来过医院，设备检修记录全部登记在册可查。",
                "2.你对样本保存温度怎么看？":"日常实验流转样本标准存放温度就是-20℃，超低温冰箱仅限研究员取用珍贵标本，我只负责机器日常维护。",
                "3.了解吸入式麻醉剂吗？":"精通通风管路构造，但麻醉药品归药房管理，规章制度严禁我们设备岗人员私自领用、存放、使用麻醉药剂。",
                "4.你认为谁嫌疑最大？":"张研究员负责该项目经费，近期项目资金濒临到期，很可能为了挽回经济损失私自盗取样本卖给校外药企。"}[q]
            st.session_state.talk_txt = ans
            st.session_state.show_ai_check = False
            st.rerun()
    if st.session_state.talk_txt:
        st.success(f"嫌疑人供述：{st.session_state.talk_txt}")
        if st.button("🤖AI自动筛查口供漏洞",use_container_width=True):
            st.session_state.leak_analysis = ai_check_confession_leak(name,st.session_state.talk_txt,st.session_state.evidence_list)
            st.session_state.show_ai_check = True
        if st.session_state.show_ai_check:
            st.markdown(f"<span class='blue-text'>【AI漏洞识别结果】{st.session_state.leak_analysis}</span>",unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("返回嫌疑人列表", use_container_width=True):
        jump("sus_list")

#5指认页
elif st.session_state.page == "judge_page":
    if not st.session_state.vid_finish:
        v = load_vid(VIDEO["judge"])
        if v:
            st.video(v, autoplay=True, muted=True, loop=False)
            time.sleep(5)
            st.session_state.vid_finish = True
            st.rerun()
    else:
        bg = img_to_base64(BG["judge"])
        st.markdown(f'<style>.stApp{{background-image:url("data:image/jpg;base64,{bg}");}}</style>', unsafe_allow_html=True)
        st.title("⚖️最终指认 · 锁定真凶")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("指认张研究员", use_container_width=True): jump("win_end")
        with c2:
            if st.button("指认刘实习生", use_container_width=True): jump("lose1_end")
        with c3:
            if st.button("指认王技术员", use_container_width=True): jump("lose2_end")
        if st.button("返回审问", use_container_width=True): jump("ask_page")

# ========== 结局页：文字黑色，无黑框 ==========
elif st.session_state.page == "win_end":
    v = load_vid(VIDEO["win"])
    if v:
        st.video(v, autoplay=True, muted=True, loop=False)
    st.markdown("""<style>.end-text *{color:#000 !important;}</style>""",unsafe_allow_html=True)
    st.markdown('<div class="suspense-card end-text">', unsafe_allow_html=True)
    st.title("🎉真相大白 · 案件侦破")
    st.markdown("你成功抓获张研究员！他因项目科研经费即将到期，私自修改样本备案，盗取样本卖给校外商业机构获利，利用麻醉剂放倒管理员、关闭监控完成作案，并刻意栽赃另外两人。")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("重新开始游戏", use_container_width=True):
        st.session_state.clear()
        jump("start")

elif st.session_state.page == "lose1_end":
    v = load_vid(VIDEO["lose_liu"])
    if v:
        st.video(v, autoplay=True, muted=True, loop=False)
    st.markdown("""<style>.end-text *{color:#000 !important;}</style>""",unsafe_allow_html=True)
    st.markdown('<div class="suspense-card end-text">', unsafe_allow_html=True)
    st.title("❌推理失误 · 冤枉实习生")
    st.markdown("无辜的刘实习生被错误定罪，真凶张研究员携样本潜逃。")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("重新开始游戏", use_container_width=True):
        st.session_state.clear()
        jump("start")

elif st.session_state.page == "lose2_end":
    v = load_vid(VIDEO["lose_wang"])
    if v:
        st.video(v, autoplay=True, muted=True, loop=False)
    st.markdown("""<style>.end-text *{color:#000 !important;}</style>""",unsafe_allow_html=True)
    st.markdown('<div class="suspense-card end-text">', unsafe_allow_html=True)
    st.title("❌推理失误 · 错怪技术员")
    st.markdown("拥有权限不代表罪犯，王技术员被冤枉，真凶逃脱。")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("重新开始游戏", use_container_width=True):
        st.session_state.clear()
        jump("start")