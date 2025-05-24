import os
import uuid
import base64
import requests
from PIL import Image as PILImage
import streamlit as st

# -----------------------------------------
# Local Ollama LLM Client
# -----------------------------------------
class OllamaLLM:
    def __init__(self, model_name="llava"):
        self.model_name = model_name
        self.endpoint = "http://localhost:11434/api/generate"

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def generate(self, prompt, image_path):
        encoded_image = self._encode_image(image_path)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "images": [encoded_image],
            "stream": False,
        }
        response = requests.post(self.endpoint, json=payload)
        if response.ok:
            return response.json().get("response", "")
        else:
            raise Exception(f"Ollama Error: {response.text}")

# -----------------------------------------
# Bengali Medical Prompts
# -----------------------------------------
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

# -----------------------------------------
# Ollama Setup and Agent Mapping
# -----------------------------------------
ollama_model = OllamaLLM(model_name="llava")

agent_options = {
    "Eye Doctor": ("Ophthalmology Analysis", ophthalmology_query),
    "Cardiology Doctor": ("Cardiology Analysis", cardiology_query),
    "Orthopedics Specialist": ("Orthopedics Analysis", orthopedics_query),
    "Medicine Doctor (Last Opinion)": ("Last Opinion Analysis", medicine_last_opinion_query)
}

# -----------------------------------------
# Image Analyzer Function
# -----------------------------------------
def analyze_medical_image(image_path, selected_agents):
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    temp_path = f"temp_resized_image_{uuid.uuid4()}.png"
    resized_image.save(temp_path)

    reports = {}
    try:
        for agent_name, query_text in selected_agents:
            response = ollama_model.generate(query_text, temp_path)
            reports[agent_name] = response
    except Exception as e:
        reports["Error"] = f"⚠️ বিশ্লেষণ ত্রুটি: {e}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return reports

# -----------------------------------------
# Streamlit UI Setup
# -----------------------------------------
st.set_page_config(page_title="মেডিকেল ইমেজ বিশ্লেষণ", layout="centered")
st.title("🩺 NAD - মেডিকেল ইমেজ বিশ্লেষণ টুল 🔬")
st.markdown(
    """
    স্বাগতম **Next AI-Assistant Doctor  - NAD ! ** আমাদের মেডিকেল ইমেজ বিশ্লেষণ টুলে! 📸  

    একটি মেডিকেল ইমেজ (রেটিনাল স্ক্যান, ইকোকার্ডিওগ্রাম, এক্স-রে ইত্যাদি) আপলোড করুন। আমাদের AI-পাওয়ার্ড সিস্টেম চারজন বিশেষজ্ঞ (চক্ষু বিশেষজ্ঞ, কার্ডিওলজিস্ট, অর্থোপেডিক বিশেষজ্ঞ এবং ইন্টারনাল মেডিসিন বিশেষজ্ঞ) দ্বারা বিশ্লেষণ করে বিস্তারিত রিপোর্ট দিবে।

    চলুন শুরু করি!
    """
)

st.sidebar.header("আপনার মেডিকেল ইমেজ আপলোড করুন:")
uploaded_file = st.sidebar.file_uploader("ইমেজ নির্বাচন করুন", type=["jpg", "jpeg", "png", "bmp", "gif"])

st.sidebar.header("বিশ্লেষণের জন্য এজেন্ট নির্বাচন করুন:")
selected_agent_names = st.sidebar.multiselect(
    "এজেন্ট নির্বাচন করুন",
    options=list(agent_options.keys()),
    default=["Eye Doctor"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="আপলোড করা ইমেজ", use_container_width=True)
    if st.sidebar.button("🔍 বিশ্লেষণ শুরু করুন"):
        if not selected_agent_names:
            st.error("⚠️ অন্তত একটি এজেন্ট নির্বাচন করুন।")
        else:
            with st.spinner("🔍 ইমেজ বিশ্লেষণ চলছে... দয়া করে অপেক্ষা করুন....."):
                image_path = f"temp_image_{uuid.uuid4()}.{uploaded_file.type.split('/')[1]}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                selected_agents = [(name, agent_options[name][1]) for name in selected_agent_names]
                reports = analyze_medical_image(image_path, selected_agents)

                st.subheader("📋 বিশ্লেষণ রিপোর্ট")
                for agent_name, report in reports.items():
                    st.markdown(f"### {agent_name}")
                    st.markdown(report, unsafe_allow_html=True)

                if os.path.exists(image_path):
                    os.remove(image_path)
else:
    st.warning("⚠️ বিশ্লেষণ শুরুর জন্য দয়া করে একটি মেডিকেল ইমেজ আপলোড করুন।")
