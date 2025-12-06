import streamlit as st
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Thêm thư mục gốc của project vào Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from workflows.orchestrator_workflow import workflow
except ImportError as e:
    st.error(f"⚠️ Lỗi import module: {e}")
    st.info("Vui lòng đảm bảo bạn đang chạy ứng dụng từ thư mục đúng và các module cần thiết đã được cài đặt.")
    st.stop()

# Cấu hình trang
st.set_page_config(
    page_title="Insurance Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .example-btn {
        margin: 0.25rem 0;
    }
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("""
    <div class="header-container">
        <h1>🏥 Insurance Assistant Chatbot</h1>
        <p>Xin chào! Tôi có thể giúp bạn về các vấn đề bảo hiểm. Hãy đặt câu hỏi của bạn!</p>
    </div>
""", unsafe_allow_html=True)

# Function xử lý tin nhắn
async def process_message(query: str) -> str:
    """Process user message and return bot response"""
    try:
        result = await workflow.run(query)
        
        if result and "messages" in result and len(result["messages"]) > 0:
            # Tìm message không phải từ Orchestrator
            for msg in reversed(result["messages"]):
                if hasattr(msg, 'content'):
                    content = msg.content
                    
                    # Handle list content
                    if isinstance(content, list):
                        response = ""
                        for item in content:
                            if isinstance(item, dict) and 'text' in item:
                                response += item['text']
                            elif isinstance(item, str):
                                response += item
                        content = response if response else str(content)
                    
                    # Skip Orchestrator messages
                    if isinstance(content, str) and not content.startswith("[Orchestrator]"):
                        return content
        
        return "Xin lỗi, tôi không thể xử lý yêu cầu của bạn lúc này."
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        import traceback
        traceback.print_exc()
        return f"Đã xảy ra lỗi: {str(e)}"

def add_message(role: str, content: str):
    """Add message to chat history"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

# Hiển thị chat history với st.chat_message
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.caption(message["timestamp"])

# Chat input - ĐẶT Ở CUỐI, SAU KHI HIỂN THỊ MESSAGES
if not st.session_state.processing:
    user_input = st.chat_input("Nhập câu hỏi của bạn...", key="chat_input")
    
    if user_input:
        # Đánh dấu đang xử lý
        st.session_state.processing = True
        
        # Thêm tin nhắn của user
        add_message("user", user_input)
        
        # Hiển thị tin nhắn user ngay lập tức
        with st.chat_message("user"):
            st.markdown(user_input)
            st.caption(datetime.now().strftime("%H:%M:%S"))
        
        # Hiển thị spinner và xử lý
        with st.chat_message("assistant"):
            with st.spinner("Đang xử lý..."):
                response = asyncio.run(process_message(user_input))
            
            st.markdown(response)
            st.caption(datetime.now().strftime("%H:%M:%S"))
        
        # Lưu response vào messages
        add_message("assistant", response)
        
        # Reset processing flag
        st.session_state.processing = False
        
        # Rerun để clear input
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Tùy chọn")
    
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.processing = False
        st.rerun()
    
    st.markdown("---")
    
    # Statistics
    if st.session_state.messages:
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.markdown("### 📊 Thống kê")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tổng tin nhắn", total_messages)
        with col2:
            st.metric("Câu hỏi", user_messages)
    
    st.markdown("---")
    st.markdown("### 📋 Về ứng dụng")
    st.markdown("""
    Ứng dụng chatbot này giúp bạn:
    - ❓ Trả lời câu hỏi về bảo hiểm
    - 👥 Quản lý thông tin khách hàng
    - 💡 Gợi ý sản phẩm phù hợp
    - 🔍 Tra cứu kiến thức từ tài liệu
    """)
    
    st.markdown("---")
    st.markdown("### 💬 Ví dụ câu hỏi")
    
    example_questions = [
        "Bảo hiểm nhân thọ là gì?",
        "Tìm khách hàng John Smith và gợi ý sản phẩm",
        "Quyền lợi bảo hiểm sức khỏe",
        "Tôi muốn mua bảo hiểm cho gia đình"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"💭 {question}", key=f"example_{i}", use_container_width=True):
            # Thêm vào messages
            add_message("user", question)
            
            # Hiển thị và xử lý
            with st.chat_message("user"):
                st.markdown(question)
                st.caption(datetime.now().strftime("%H:%M:%S"))
            
            with st.chat_message("assistant"):
                with st.spinner("Đang xử lý..."):
                    response = asyncio.run(process_message(question))
                st.markdown(response)
                st.caption(datetime.now().strftime("%H:%M:%S"))
            
            add_message("assistant", response)
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Insurance Chatbot © 2024 | Powered by LangGraph & Gemini</p>
    </div>
""", unsafe_allow_html=True)