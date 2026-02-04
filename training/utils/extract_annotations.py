import asyncio
import logging
from agentlightning.store.client_server import LightningStoreClient
from agentlightning.semconv import AGL_ANNOTATION

# Cấu hình logging để thấy chi tiết quá trình truy vấn
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def extract_annotations(rollout_id: str, store_url: str = "http://localhost:4747"):
    """
    Trích xuất các `agentlightning.annotation` từ một rollout cụ thể.
    """
    # 1. Khởi tạo client kết nối tới Lightning Store (Dashboard)
    client = LightningStoreClient(store_url)
    
    try:
        logger.info(f"🔍 Đang truy vấn spans cho rollout: {rollout_id}")
        
        # 2. Truy vấn các spans có tên là 'agentlightning.annotation'
        # Hoặc có thể query tất cả và lọc dựa trên attributes
        result = await client.query_spans(
            rollout_id=rollout_id,
            name=AGL_ANNOTATION, # agentlightning.annotation
            limit=-1 # Lấy tất cả
        )
        
        annotations = result.items
        logger.info(f"✅ Tìm thấy {len(annotations)} annotations.")
        
        for span in annotations:
            print(f"\n--- Annotation Span ID: {span.span_id} ---")
            print(f"Name: {span.name}")
            
            # 3. Trích xuất dữ liệu từ attributes
            # Dữ liệu thực tế thường nằm trong span.attributes
            if span.attributes:
                print("Attributes:")
                for key, value in span.attributes.items():
                    print(f"  - {key}: {value}")
            
    except Exception as e:
        logger.error(f"❌ Lỗi khi trích xuất: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    # Thay thế rollout_id bằng ID thực tế bạn muốn kiểm tra từ dashboard
    # Ví dụ: "rollout_01j7..."
    TARGET_ROLLOUT_ID = "YOUR_ROLLOUT_ID_HERE" 
    
    # Chạy async script
    asyncio.run(extract_annotations(TARGET_ROLLOUT_ID))
