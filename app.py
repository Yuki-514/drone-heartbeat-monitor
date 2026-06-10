import streamlit as st
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

# 页面基础设置
st.set_page_config(page_title="无人机心跳监测可视化", layout="wide")
st.title("基于AI编程-无人机通信心跳监测系统")

# 初始化会话存储数据
if "heartbeat_data" not in st.session_state:
    st.session_state.heartbeat_data = []
if "seq_num" not in st.session_state:
    st.session_state.seq_num = 0
if "last_receive_time" not in st.session_state:
    st.session_state.last_receive_time = time.time()
if "is_offline" not in st.session_state:
    st.session_state.is_offline = False

# 侧边栏控制按钮
col1, col2 = st.sidebar.columns(2)
start_btn = col1.button("启动无人机发送心跳")
stop_btn = col2.button("停止模拟")

data_container = st.empty()
chart_container = st.empty()
alert_box = st.empty()

# 心跳循环模拟
if start_btn:
    st.sidebar.success("模拟发送中...")
    while True:
        current_time = time.time()
        # 生成心跳包
        st.session_state.seq_num += 1
        now_dt = datetime.now().strftime("%H:%M:%S")
        packet = {
            "序号": st.session_state.seq_num,
            "接收时间": now_dt,
            "时间戳": current_time
        }
        st.session_state.heartbeat_data.append(packet)
        st.session_state.last_receive_time = current_time
        st.session_state.is_offline = False

        # 断线检测：超过3秒无心跳报警
        gap = current_time - st.session_state.last_receive_time
        if gap > 3:
            st.session_state.is_offline = True
            alert_box.error(f"⚠️ 断线告警：已超过{round(gap,1)}秒未收到心跳包！")
        else:
            alert_box.success(f"✅ 通信正常，距离上次心跳间隔 {round(gap,1)}s")

        # 数据表格展示
        df = pd.DataFrame(st.session_state.heartbeat_data)
        data_container.dataframe(df.tail(15), use_container_width=True)

        # 折线可视化图表
        fig = px.line(df, x="接收时间", y="序号", title="心跳包序号随时间变化曲线")
        chart_container.plotly_chart(fig, use_container_width=True)

        time.sleep(1)
        if stop_btn:
            st.sidebar.info("模拟已停止")
            break
