import requests
import re
import urllib.parse
import streamlit as st

# Thông tin Affiliate của bạn
MY_AFFILIATE_ID = "17310280315"
MY_SUB_ID = "KEM_REVIEW"

def get_original_link(url):
    """Hàm bung link rút gọn"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # requests.get sẽ tự động theo dõi redirect (allow_redirects=True mặc định)
        # response.url sẽ chứa đường link đích cuối cùng
        response = requests.get(url, headers=headers, timeout=10)
        return response.url
    except Exception as e:
        return ""

def extract_shopee_ids(url):
    """Hàm bóc tách Shop ID và Item ID"""
    # Bước 1: Làm sạch link, bỏ params
    clean_url = url.split('?')[0].strip()
    
    # Bước 2: Dùng Regex kiểm tra các định dạng
    # Case 1: Dạng -i.ShopID.ItemID
    match1 = re.search(r'-i\.(\d+)\.(\d+)', clean_url)
    if match1:
        return match1.group(1), match1.group(2)
        
    # Case 2: Dạng shopee.vn/tên-shop/ShopID/ItemID
    match2 = re.search(r'shopee\.vn/[^/]+/(\d+)/(\d+)', clean_url)
    if match2:
        return match2.group(1), match2.group(2)
        
    # Case 3: Dạng /product/ShopID/ItemID hoặc /ShopID/ItemID cơ bản
    match3 = re.search(r'/(\d+)/(\d+)', clean_url)
    if match3:
        return match3.group(1), match3.group(2)
        
    return "", ""

def generate_affiliate_link(shop_id, item_id):
    """Hàm tạo link Affiliate"""
    origin_product_link = f"https://shopee.vn/product/{shop_id}/{item_id}"
    
    # Mã hóa URL (tương đương Uri.EscapeDataString trong C#)
    encoded_link = urllib.parse.quote(origin_product_link, safe='')
    
    final_url = f"https://s.shopee.vn/an_redir?origin_link={encoded_link}&affiliate_id={MY_AFFILIATE_ID}&sub_id={MY_SUB_ID}"
    return final_url

def process_conversion(input_url):
    """Hàm tổng hợp quy trình"""
    full_url = input_url
    
    # Nếu là link rút gọn thì bung link
    if "s.shopee.vn" in input_url or "shope.ee" in input_url or "vn.shp.ee" in input_url:
        full_url = get_original_link(input_url)
        
    if not full_url:
        return False, "Lỗi: Không thể lấy được link gốc, vui lòng kiểm tra lại mạng hoặc link."
        
    # Bóc tách ID
    shop_id, item_id = extract_shopee_ids(full_url)
    
    if shop_id and item_id:
        final_link = generate_affiliate_link(shop_id, item_id)
        return True, final_link
    else:
        return False, "Lỗi: Không tìm thấy Shop ID và Item ID trong link này."
    # ==========================================
# PHẦN GIAO DIỆN WEB (UI) BẰNG STREAMLIT
# ==========================================

# Cài đặt tiêu đề trang web
st.set_page_config(page_title="Đổi Link Shopee", page_icon="🛍️")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;} /* Ẩn toàn bộ thanh header chứa icon GitHub */
            [data-testid="stToolbar"] {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ff5722;'>🛍️ ĐỔI LINK SHOPEE ÁP MÃ 20% 25%</h2>", unsafe_allow_html=True)
st.write("---")

# Ô nhập liệu (Input field)
input_url = st.text_input("Dán link Shopee vào đây:", placeholder="https://shopee.vn/...")

# Nút bấm (Button)
if st.button("CHUYỂN ĐỔI NGAY", type="primary", use_container_width=True):
    if not input_url:
        st.warning("Vui lòng dán link cần chuyển đổi vào ô trống!")
    else:
        with st.spinner('Đang xử lý chuyển đổi...'):
            success, result = process_conversion(input_url)
            
            if success:
                st.success("✅ Đã chuyển đổi xong")
                
                # Hiển thị link đã chuyển đổi trong một ô copy dễ nhìn
                st.code(result, language="http")
                
                # Optional: Bạn có thể thêm thẻ hiển thị thông tin như trong ảnh tại đây
                st.info("Bây giờ bạn có thể sao chép link trên để chia sẻ lấy hoa hồng!")
            else:
                st.error(result)