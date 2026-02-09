"""
Streamlit Demo Application for Agno AI Agent.

Giao diện web tương tác để demo và hiển thị đầy đủ quá trình hoạt động của agent.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import logging
import importlib
from dotenv import load_dotenv
from datetime import datetime
import time
import json



from core.config import AgentConfig
from core.agent_manager import AgnoAgentManager
from app.streamlit_helper import (
    format_timestamp,
    get_session_list,
    calculate_analytics,
    format_tool_call_display,
    export_conversation,
    read_log_file,
    parse_logs_by_cycle
)


# ========================================
# Page Configuration
# ========================================
st.set_page_config(
    page_title="Agno AI Agent Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# Logging Configuration
# ========================================
# Configure logging to write to output.log
log_file_path = Path(__file__).parent.parent / "output.log"

# Configure root logger to capture everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()  # Also print to console
    ],
    force=True  # Override any existing logging config
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Also configure agno and core module loggers to DEBUG
logging.getLogger('agno').setLevel(logging.DEBUG)
logging.getLogger('core').setLevel(logging.DEBUG)
logging.getLogger('training').setLevel(logging.DEBUG)



# ========================================
# Initialize Session State
# ========================================
def initialize_session_state():
    """Khởi tạo session state cho Streamlit."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'agent_manager' not in st.session_state:
        st.session_state.agent_manager = None
    
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = f"streamlit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if 'config' not in st.session_state:
        st.session_state.config = None
    
    if 'tool_calls' not in st.session_state:
        st.session_state.tool_calls = []
    
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False

    if 'agent_instructions' not in st.session_state:
        # Import default instructions if not in session state
        from core.prompts import DEFAULT_AGENT_INSTRUCTIONS
        st.session_state.agent_instructions = "\n".join(DEFAULT_AGENT_INSTRUCTIONS)




# ========================================
# Agent Initialization
# ========================================
def initialize_agent(session_id: str, debug_mode: bool = False, custom_instructions: str = None):
    """
    Khởi tạo agent với cấu hình.
    
    Args:
        session_id: Session ID
        debug_mode: Enable debug mode
        custom_instructions: Custom instructions for the agent
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Create config
        config = AgentConfig()
        config.session_id = session_id
        config.debug_mode = debug_mode
        
        # Parse instructions from string to list if provided
        instructions_list = None
        if custom_instructions:
            instructions_list = [line.strip() for line in custom_instructions.split('\n') if line.strip()]
        
        # Create and initialize agent manager
        import core.agent_manager
        import core.config
        importlib.reload(core.config)
        importlib.reload(core.agent_manager)
        
        from core.agent_manager import AgnoAgentManager
        from core.config import AgentConfig
        
        manager = AgnoAgentManager(config)
        manager.initialize(custom_instructions=instructions_list)
        
        st.session_state.agent_manager = manager
        st.session_state.config = config
        
        return True
    except Exception as e:
        st.error(f"❌ Lỗi khởi tạo agent: {e}")
        logger.error(f"Agent initialization error: {e}", exc_info=True)
        return False


# ========================================
# Sidebar
# ========================================
def render_sidebar():
    """Render sidebar with tabs organization."""
    with st.sidebar:
        st.title("🤖 Agno Agent")
        st.markdown("---")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "⚙️ Config",
            "📋 Sessions", 
            "🎓 Training",
            "📊 Analytics",
            "🔍 Process",
            "📋 Logs"
        ])
        
        # Tab 1: Configuration
        with tab1:
            st.subheader("Agent Configuration")
            
            # Session ID
            session_id = st.text_input(
                "Session ID",
                value=st.session_state.current_session_id,
                help="ID của phiên hội thoại"
            )
            
            # Debug mode
            debug_mode = st.checkbox(
                "Debug Mode",
                value=st.session_state.debug_mode,
                help="Hiển thị thông tin debug chi tiết"
            )
            
            # Agent Instructions
            agent_instructions = st.text_area(
                "Agent Instructions",
                value=st.session_state.agent_instructions,
                help="Các chỉ dẫn cho agent (mỗi dòng một chỉ dẫn)",
                height=150
            )
            
            # Initialize/Reinitialize button
            if st.button("🔄 Khởi tạo Agent", type="primary", use_container_width=True):
                with st.spinner("Đang khởi tạo agent..."):
                    if initialize_agent(session_id, debug_mode, agent_instructions):
                        st.session_state.current_session_id = session_id
                        st.session_state.debug_mode = debug_mode
                        st.session_state.agent_instructions = agent_instructions
                        st.success("✅ Agent đã sẵn sàng!")
                        st.rerun()
        
        # Tab 2: Session Management
        with tab2:
            st.subheader("Session Management")
            
            if st.session_state.config:
                db_path = st.session_state.config.db_path
                sessions = get_session_list(db_path)
                
                if sessions:
                    st.write(f"**Total Sessions:** {len(sessions)}")
                    st.markdown("---")
                    
                    for session in sessions[:5]:  # Show last 5 sessions
                        with st.expander(f"📝 {session['id'][:20]}..."):
                            st.write(f"**Messages:** {session['message_count']}")
                            st.write(f"**Created:** {session.get('created_at', 'N/A')}")
                else:
                    st.info("No sessions found")
            
            st.markdown("---")
            
            # Clear conversation button
            if st.button("🗑️ Xóa hội thoại hiện tại", type="secondary", use_container_width=True):
                st.session_state.messages = []
                st.session_state.tool_calls = []
                st.success("✅ Đã xóa hội thoại!")
                st.rerun()
        
        # Tab 3: Training
        with tab3:
            st.subheader("Agent Training")
            
            st.info("🎓 Train your agent with Agent Lightning")
            
            # Training configuration
            col1, col2 = st.columns(2)
            with col1:
                train_iterations = st.number_input("Iterations", min_value=1, max_value=50, value=10, key="train_iter")
            with col2:
                train_size = st.number_input("Train Size", min_value=5, max_value=100, value=20, key="train_size")
            
            st.markdown("---")
            
            if st.button("🚀 Start Training", type="primary", use_container_width=True):
                import subprocess
                import sys
                
                with st.spinner("� Training in progress..."):
                    try:
                        # Build training command
                        python_exe = sys.executable
                        train_cmd = [
                            python_exe, 
                            "-m", 
                            "training.train",
                            "--iterations", str(train_iterations),
                            "--train-size", str(train_size),
                            "--val-size", str(train_size // 2)
                        ]
                        
                        # Show command being executed
                        st.code(" ".join(train_cmd), language="bash")
                        
                        # Run training
                        result = subprocess.run(
                            train_cmd,
                            cwd=Path(__file__).parent.parent,
                            capture_output=True,
                            text=True,
                            timeout=600  # 10 minute timeout
                        )
                        
                        # Show results
                        if result.returncode == 0:
                            st.success("✅ Training completed successfully!")
                            
                            # Show output
                            with st.expander("📋 Training Output", expanded=True):
                                st.code(result.stdout, language="log")
                            
                            # Reload page to update prompt management section
                            st.balloons()
                            st.info("🔄 Reloading to show new best prompt...")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Training failed!")
                            with st.expander("🔍 Error Details", expanded=True):
                                st.code(result.stderr, language="log")
                            
                    except subprocess.TimeoutExpired:
                        st.error("⏱️ Training timeout (>10 minutes)")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        logger.error(f"Training execution error: {e}", exc_info=True)

        
        # Tab 4: Analytics
        with tab4:
            st.subheader("Statistics")
            
            if st.session_state.config:
                analytics = calculate_analytics(st.session_state.config.db_path)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sessions", analytics['total_sessions'])
                with col2:
                    st.metric("Messages", analytics['total_messages'])
                
                if analytics['tool_usage']:
                    st.markdown("---")
                    st.write("**🔧 Tool Usage**")
                    for tool, count in analytics['tool_usage'].items():
                        st.write(f"• **{tool}:** {count}x")
            else:
                st.info("Initialize agent to view analytics")
        
        # Tab 5: Process Log
        with tab5:
            st.subheader("Process Visualization")
            
            if st.session_state.tool_calls:
                st.write(f"**Total Tool Calls:** {len(st.session_state.tool_calls)}")
                st.markdown("---")
                
                for i, tool_call in enumerate(st.session_state.tool_calls[-5:], 1):  # Last 5
                    with st.expander(f"Call #{i} - {tool_call['name']}"):
                        st.markdown(format_tool_call_display(
                            tool_call['name'],
                            tool_call.get('arguments', '{}'),
                            tool_call.get('result')
                        ))
            else:
                st.info("No tool calls yet")
        
        # Tab 6: Debug Logs
        with tab6:
            st.subheader("Debug Logs")            
            # Read all logs (no line limit)
            log_file_path = Path(__file__).parent.parent / "output.log"
            log_lines = read_log_file(log_path=str(log_file_path), max_lines=None)
            
            if log_lines:
                # Parse logs into Q&A cycles
                cycles = parse_logs_by_cycle(log_lines)
                
                if cycles:
                    st.write(f"**Total Q&A Cycles:** {len(cycles)}")
                    st.markdown("---")
                    
                    # Display each cycle in a collapsible expander (newest first)
                    for i, cycle in enumerate(cycles, 1):
                        # Create title for expander
                        question = cycle.get('question', 'Unknown question')
                        timestamp = cycle.get('timestamp', '')
                        run_id = cycle.get('run_id', '')
                        
                        # Truncate question if too long
                        if question and len(question) > 60:
                            question_display = question[:60] + "..."
                        else:
                            question_display = question if question else 'Unknown question'
                        
                        # Create expander title with timestamp and question
                        expander_title = f"🔄 Cycle #{i}"
                        if timestamp:
                            expander_title += f" - {timestamp}"
                        if question_display:
                            expander_title += f" | {question_display}"
                        
                        with st.expander(expander_title, expanded=(i == 1)):  # First one expanded by default
                            # Show cycle metadata
                            if run_id:
                                st.caption(f"**Run ID:** `{run_id}`")
                            if question and question != question_display:
                                st.caption(f"**Full Question:** {question}")
                            
                            st.markdown("---")
                            
                            # Display logs for this cycle
                            cycle_logs = "".join(cycle['logs'])
                            st.code(cycle_logs, language="log", line_numbers=False)
                else:
                    # No cycles detected, show all logs
                    st.info("No Q&A cycles detected. Showing all logs:")
                    log_text = "".join(log_lines)
                    st.code(log_text, language="log", line_numbers=False)
            else:
                st.info("No logs available")
            
         
        
        # Footer
        st.markdown("---")
        st.caption("Powered by Agno AI Framework")
        st.caption("Model: Gemini 2.0 Flash")


# ========================================
# Main Chat Interface
# ========================================
def render_chat_interface():
    """Render main chat interface."""
    st.title("💬 Chat với Agno Agent")
    
    # Display agent status
    if st.session_state.agent_manager is None:
        st.warning("⚠️ Agent chưa được khởi tạo. Vui lòng khởi tạo agent ở sidebar.")
        st.info("👈 Nhấn nút '🔄 Khởi tạo Agent' ở sidebar để bắt đầu.")
        return
    else:
        st.success("✅ Agent đã sẵn sàng!")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Agent đang suy nghĩ..."):
                try:
                    # Run agent
                    agent = st.session_state.agent_manager.agent
                    response = agent.run(prompt)
                    
                    # Extract response content
                    response_content = response.content if hasattr(response, 'content') else str(response)
                    
                    # Display response
                    st.markdown(response_content)
                    
                    # Add to conversation history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content
                    })
                    
                    # Track tool calls if available
                    if hasattr(response, 'messages'):
                        for msg in response.messages:
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    # Handle both dict and object formats
                                    if isinstance(tool_call, dict):
                                        tool_name = tool_call.get('function', {}).get('name', 'unknown')
                                        tool_args = tool_call.get('function', {}).get('arguments', '{}')
                                    else:
                                        tool_name = tool_call.function.name if hasattr(tool_call, 'function') else 'unknown'
                                        tool_args = tool_call.function.arguments if hasattr(tool_call, 'function') else '{}'
                                    
                                    st.session_state.tool_calls.append({
                                        'name': tool_name,
                                        'arguments': tool_args,
                                        'timestamp': datetime.now().isoformat()
                                    })
                    
                    # Refresh to update sidebar
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"❌ Lỗi: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    logger.error(f"Error processing question: {e}", exc_info=True)



        

# ========================================
# Main Application
# ========================================
def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat_interface()

    

if __name__ == "__main__":
    main()
