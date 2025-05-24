import os
import uuid
from PIL import Image as PILImage
import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="🩺 NAD - মেডিকেল ইমেজ বিশ্লেষণ", layout="centered")

# Set API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCQVrag8PvuNMYY5RGLdlAnSBap9_2_3DY"

# Load Queries
# Ophthalmology (Eye Doctor) Query in Bengali
ophthalmology_query = """
**আপনার সমস্ত উত্তর বাংলায় দিন।**

আপনি একজন অভিজ্ঞ চক্ষু বিশেষজ্ঞ, যিনি রেটিনাল ইমেজিং এবং চোখের রোগ নির্ণয়ে বিশেষজ্ঞ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (রেটিনাল ফটোগ্রাফি, OCT, ফান্ডাস ইমেজ ইত্যাদি)।
- কোন চোখের অঞ্চল (রেটিনা, অপটিক ডিস্ক, ম্যাকুলা ইত্যাদি) এবং পজিশন তা বলুন।
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন।

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো সুনির্দিষ্টভাবে তুলে ধরুন (যেমন রেটিনার অবস্থা, রক্তনালীর গঠন)।
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন ডায়াবেটিক রেটিনোপ্যাথি, ম্যাকুলার ডিজেনারেশন)।
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন ম্যাকুলার পুরুত্ব) উল্লেখ করুন।

### ৩. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে।
- সম্ভাব্য অন্যান্য রোগসমূহ তালিকাভুক্ত করুন।
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন।
- জরুরি বা গুরুত্বপূর্ণ বিষয় (যেমন দৃষ্টিহানির ঝুঁকি) হাইলাইট করুন।

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন।
- চিকিৎসাগত শব্দ (যেমন ম্যাকুলা, রেটিনোপ্যাথি) সহজ করে বোঝান।
- বাস্তব জীবনের উদাহরণ ব্যবহার করুন।

### ৫. গবেষণা প্রসঙ্গ
- বিশ্লেষণ সমর্থনে ২-৩টি গুরুত্বপূর্ণ রেফারেন্স দিন। In English
"""

# Cardiology Doctor Query in Bengali
cardiology_query = """
**আপনার সমস্ত উত্তর বাংলায় দিন।**

আপনি একজন অভিজ্ঞ কার্ডিওলজিস্ট, যিনি হৃদরোগ সম্পর্কিত ইমেজিং (যেমন ইকোকার্ডিওগ্রাম, এনজিওগ্রাম) বিশ্লেষণে বিশেষজ্ঞ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (ইকোকার্ডিওগ্রাম, কার্ডিয়াক CT, এনজিওগ্রাম ইত্যাদি)।
- হৃদপিণ্ডের কোন অঞ্চল (ভাল্ভ, ভেন্ট্রিকল, করোনারি ধমনী) এবং পজিশন তা বলুন।
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন।

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো তুলে ধরুন (যেমন ভাল্ভের কার্যকারিতা, ধমনীর সংকীর্ণতা)।
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন স্টেনোসিস, ইজেকশন ফ্রাকশন অস্বাভাবিকতা)।
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন ইজেকশন ফ্রাকশন, ধমনীর ব্যাস) উল্লেখ করুন।

### ৩. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে।
- সম্ভাব্য অন্যান্য রোগ তালিকাভুক্ত করুন।
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন।
- জরুরি বিষয় (যেমন তীব্র করোনারি সিনড্রোম) হাইলাইট করুন।

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন।
- চিকিৎসাগত শব্দ (যেমন ইজেকশন ফ্রাকশন, স্টেনোসিস) সহজ করে বোঝান।
- বাস্তব উদাহরণ ব্যবহার করুন।

### ৫. গবেষণা প্রসঙ্গ
- বিশ্লেষণ সমর্থনে ২-৩টি গুরুত্বপূর্ণ রেফারেন্স দিন। In English
"""

# Orthopedics Specialist Query in Bengali
orthopedics_query = """
**আপনার সমস্ত উত্তর বাংলায় দিন।**

আপনি একজন অভিজ্ঞ অর্থোপেডিক বিশেষজ্ঞ, যিনি হাড় এবং জয়েন্ট সম্পর্কিত ইমেজিং (যেমন এক্স-রে, MRI, CT স্ক্যান) বিশ্লেষণে দক্ষ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (এক্স-রে, MRI, CT স্ক্যান ইত্যাদি)।
- কোন শারীরিক অঞ্চল (হাড়, জয়েন্ট, মেরুদণ্ড, ফ্র্যাকচার সাইট) এবং পজিশন তা বলুন।
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন।

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো তুলে ধরুন (যেমন হাড়ের গঠন, জয়েন্টের স্থান, ফ্র্যাকচারের ধরন)।
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন ফ্র্যাকচার, অস্টিওআর্থ্রাইটিস, ডিসলোকেশন)।
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন জয়েন্ট স্পেস প্রস্থ, ফ্র্যাকচারের দৈর্ঘ্য) উল্লেখ করুন।

### �３. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে।
- সম্ভাব্য অন্যান্য রোগ তালিকাভুক্ত করুন।
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন।
- জরুরি বিষয় (যেমন ফ্র্যাকচারের স্থানচ্যুতি, সংক্রমণের ঝুঁকি) হাইলাইট করুন।

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন।
- চিকিৎসাগত শব্দ (যেমন ফ্র্যাকচার, অস্টিওআর্থ্রাইটিস) সহজ করে বোঝান।
- বাস্তব উদাহরণ ব্যবহার করুন।

### ৫. গবেষণা প্রসঙ্গ
- বিশ্লেষণ সমর্থনে ২-৩টি গুরুত্বপূর্ণ রেফারেন্স দিন। In English
"""

# Medicine Doctor (Last Opinion) Query in Bengali
medicine_last_opinion_query = """
**আপনার সমস্ত উত্তর বাংলায় দিন।**

আপনি একজন অভিজ্ঞ ইন্টারনাল মেডিসিন বিশেষজ্ঞ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং রোগীর সমস্যার সাথে সম্পর্কিত নির্দিষ্ট বিশেষজ্ঞদের (চক্ষু বিশেষজ্ঞ, কার্ডিওলজিস্ট, অর্থোপেডিক বিশেষজ্ঞ) উল্লেখ করুন। শুধুমাত্র সম্পর্কিত বিশেষজ্ঞদের নাম এবং তাদের প্রাসঙ্গিকতার সংক্ষিপ্ত ব্যাখ্যা দিন। বিস্তারিত বিশ্লেষণ বা অন্যান্য বিষয় (যেমন চিত্রের ধরন, পর্যবেক্ষণ, রোগ নির্ণয়, রোগীর ব্যাখ্যা, গবেষণা রেফারেন্স) অন্তর্ভুক্ত করবেন না।
"""

# Initialize Agents
ophthalmology_agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGoTools()], markdown=True)
cardiology_agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGoTools()], markdown=True)
orthopedics_agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGoTools()], markdown=True)
medicine_last_opinion_agent = Agent(model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGoTools()], markdown=True)

agent_options = {
    "Eye Doctor": (ophthalmology_agent, "Ophthalmology Analysis", ophthalmology_query),
    "Cardiology Doctor": (cardiology_agent, "Cardiology Analysis", cardiology_query),
    "Orthopedics Specialist": (orthopedics_agent, "Orthopedics Analysis", orthopedics_query),
    "Medicine Doctor (Last Opinion)": (medicine_last_opinion_agent, "Last Opinion Analysis", medicine_last_opinion_query)
}

# Initial Greeting
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "doctor", "text": "👋 স্বাগতম! আমি একজন মেডিকেল ইমেজ বিশ্লেষক। একটি ইমেজ আপলোড করুন এবং যেকোনো প্রশ্ন করুন।"})

# UI Title
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#2563EB;'>🩺 NAD - মেডিকেল ইমেজ বিশ্লেষণ</h1>
        <p style='font-size:18px;'>AI দ্বারা চালিত একটি স্মার্ট চিকিৎসা সহকারী</p>
    </div>
""", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader("👇 এখানে আপনার ইমেজ ফাইল টেনে আনুন বা ক্লিক করুন", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Agent Selection
selected_agent_names = st.multiselect(
    "👨‍⚕️ বিশ্লেষণের জন্য ডাক্তার নির্বাচন করুন",
    options=list(agent_options.keys()),
    default=["Eye Doctor"]
)

# Report Display
def display_report_card(title, content):
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h4>{title}</h4>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

# Image Analysis Logic
def analyze_medical_image(image_path, selected_agents):
    image = PILImage.open(image_path)
    aspect_ratio = image.width / image.height
    resized_image = image.resize((500, int(500 / aspect_ratio)))
    temp_path = f"temp_resized_{uuid.uuid4()}.png"
    resized_image.save(temp_path)
    agno_image = AgnoImage(filepath=temp_path)

    reports = {}
    try:
        for agent, agent_name, query_text in selected_agents:
            response = agent.run(query_text, images=[agno_image])
            reports[agent_name] = response.content
    except Exception as e:
        reports["Error"] = f"⚠️ বিশ্লেষণ ত্রুটি: {e}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return reports

# Show Uploaded Image & Analyze
if uploaded_file is not None:
    st.image(uploaded_file, caption="আপলোড করা ইমেজ", use_container_width=True)

    if st.button("🔍 বিশ্লেষণ শুরু করুন"):
        if not selected_agent_names:
            st.error("⚠️ অন্তত একটি ডাক্তার নির্বাচন করুন।")
        else:
            with st.spinner("🔬 AI বিশ্লেষণ চলছে..."):
                image_ext = uploaded_file.type.split("/")[1]
                image_path = f"temp_input_{uuid.uuid4()}.{image_ext}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                selected_agents = [agent_options[name] for name in selected_agent_names]
                reports = analyze_medical_image(image_path, selected_agents)

                tabs = st.tabs([name for name in selected_agent_names])
                for i, name in enumerate(selected_agent_names):
                    with tabs[i]:
                        content = reports.get(agent_options[name][1], "❌ কোনো তথ্য পাওয়া যায়নি")
                        display_report_card(agent_options[name][1], content)

                os.remove(image_path)
else:
    st.warning("⚠️ দয়া করে একটি ইমেজ আপলোড করুন।")

# Chat Interface
st.markdown("## 💬 আলাপচারিতা")

# Display Chat History
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div style='text-align: right; background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0;'>{chat['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; background-color:#F0F2F6; padding:10px; border-radius:10px; margin:5px 0;'>{chat['text']}</div>", unsafe_allow_html=True)

# Input for Chat
st.markdown("---")
st.markdown("#### নতুন প্রশ্ন করুন")
chat_col1, chat_col2 = st.columns([4, 1])

with chat_col1:
    user_input = st.text_input("✍️", placeholder="আপনার প্রশ্ন লিখুন", label_visibility="collapsed", key="chat_input")
with chat_col2:
    selected_doctor = st.selectbox("ডাক্তার", options=list(agent_options.keys()), label_visibility="collapsed", index=0)

if st.button("📨 পাঠান"):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        selected_agent = agent_options[selected_doctor][0]
        response = selected_agent.run(user_input)
        st.session_state.chat_history.append({"role": "doctor", "text": response.content})
    else:
        st.warning("⚠️ প্রশ্ন লিখুন।")
