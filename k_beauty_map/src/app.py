import streamlit as st
import pandas as pd
import os
import unicodedata
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import base64
from streamlit_option_menu import option_menu

# --- Layout Configuration ---
st.set_page_config(page_title="Sample Store App", layout="wide", initial_sidebar_state="expanded")

# --- Directory Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
IMG_DIR = os.path.join(BASE_DIR, '..', 'images')

# --- Cached Data Loading ---
@st.cache_data
def load_csv_data(file_name, encoding='utf-8'):
    filepath = os.path.join(DATA_DIR, file_name)
    try:
        return pd.read_csv(filepath, encoding=encoding)
    except UnicodeDecodeError:
        return pd.read_csv(filepath, encoding='cp949')
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return pd.DataFrame()

# --- Custom CSS (Apple Minimalism typography) ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Pretendard or System UI */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        html, body, [class*="css"] {
            font-family: 'Pretendard', -apple-system, sans-serif !important;
            background-color: #F4F2FA !important;
            color: #000000 !important;
            font-weight: 400 !important;
            letter-spacing: -0.02em !important;
        }
        
        /* Ensure the main container inherits the background */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Allow clicks to pass through transparent header to the menu */
        [data-testid="stHeader"] {
            pointer-events: none;
        }
        [data-testid="stHeader"] * {
            pointer-events: auto;
        }

        /* Padding around content to avoid feeling cramped */
        .block-container {
            padding: 20px !important;
        }

        /* Sidebar Styling (Glassmorphism 20px, 0.15) */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Main Welcome Card */
        .welcome-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 4rem 3rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin: 10vh auto;
            max-width: 700px;
        }

        .welcome-text {
            font-size: 1.6rem;
            font-weight: 700;
            line-height: 1.5;
            color: #000000;
            letter-spacing: -0.02em;
        }

        /* Buttons radius & glass */
        div[data-testid="stButton"] button {
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            color: #000000 !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
            letter-spacing: -0.02em !important;
        }
        
        div[data-testid="stButton"] button:hover {
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.25) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            color: #000000 !important;
        }

        /* Map Iframe Styling to act as Glassmorphism Container */
        iframe[title="streamlit_folium.st_folium"] {
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 10px; /* gives the floating glass border around map */
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        }

        /* Product Card Styles */
        .product-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }

        .product-img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 0.8rem;
        }

        .product-title {
            font-size: 0.95rem;
            font-weight: 700 !important;
            margin: 0.2rem 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #000000;
            letter-spacing: -0.02em;
        }

        .product-price {
            font-size: 0.85rem;
            font-weight: 400 !important;
            color: #000000;
            letter-spacing: -0.02em;
        }
        
        /* Menu Heading (Overrides global h2 rules) */
        .menu-heading, .menu-heading * {
            margin-top: 1rem !important;
            margin-bottom: 0.3rem !important;
            text-align: center !important;
            color: #232A32 !important;
            font-weight: 500 !important;
            font-size: 40px !important;
            letter-spacing: 1px !important;
        }

        /* Headers and Global Text */
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        label, p, span, .stMarkdown {
            color: #000000 !important;
            font-weight: 400 !important;
            letter-spacing: -0.02em !important;
        }
        
        /* Custom Geolocation wrapper */
        .geo-container {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        .geo-label {
            font-weight: 700 !important;
            color: #000000;
            margin-left: 10px;
            font-size: 1.1rem;
            letter-spacing: -0.02em !important;
        }

        /* st.tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        .stTabs [data-baseweb="tab"] * {
            color: #000000 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            letter-spacing: -0.02em !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(255,255,255,0.2) !important;
            border-radius: 12px;
            padding-left: 20px !important;
            padding-right: 20px !important;
        }
        .stTabs [aria-selected="true"] * {
            font-weight: 600 !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #F93780 !important;
        }
        
        /* Popup HTML class scope for ensuring UI consistency */
        .custom-popup {
            font-family: 'Pretendard', -apple-system, sans-serif !important;
            padding: 10px;
        }
        .custom-popup b {
            font-size: 16px;
            font-weight: 700 !important;
            color: #000000 !important;
            letter-spacing: -0.02em !important;
        }
        .custom-popup .address {
            color: #555 !important;
            font-weight: 400 !important;
            font-size: 13px;
            margin-top: 4px;
            display: inline-block;
            letter-spacing: -0.02em !important;
        }
        .custom-popup .tag {
            color: #007AFF !important;
            font-weight: 400 !important;
            font-size: 12px;
            margin-top: 6px;
            display: inline-block;
            letter-spacing: -0.02em !important;
            word-break: keep-all;
        }
        </style>
    """, unsafe_allow_html=True)

# Helper function to find images
def find_image_path(product_name, brand_folder):
    target_dir = os.path.join(IMG_DIR, brand_folder)
    if not os.path.exists(target_dir):
        return None
        
    product_name_norm = unicodedata.normalize('NFC', str(product_name).strip()).replace(' ', '')
    
    for f in os.listdir(target_dir):
        f_norm = unicodedata.normalize('NFC', f)
        if product_name_norm in f_norm.replace(' ', ''):
            return os.path.join(target_dir, f)
            
    return None

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_product_card(product_row, brand_folder):
    name = product_row['상품명']
    price = product_row['가격']
    link = product_row.get('링크', '#')
    
    img_path = find_image_path(name, brand_folder)
    
    if img_path and os.path.exists(img_path):
        img_b64 = get_base64_of_bin_file(img_path)
        img_html = f'<img src="data:image/jpeg;base64,{img_b64}" class="product-img" alt="{name}">'
    else:
        # Placeholder if no image
        img_html = f'<div class="product-img" style="background:#e5e5ea; display:flex; align-items:center; justify-content:center; color:#86868b; font-size:0.8rem;">No Image</div>'

    html = f"""
    <a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
        <div class="product-card">
            {img_html}
            <div class="product-title" title="{name}">{name}</div>
            <div class="product-price">{price:,}원</div>
        </div>
    </a>
    """
    st.markdown(html, unsafe_allow_html=True)

def generate_popup_html(brand, name, address, tagList=None, imgUri=None):
    html = f'<div class="custom-popup"><b>[{brand}] {name}</b><br>'
    
    if imgUri and str(imgUri) != 'nan':
        img_url = str(imgUri)
        if img_url.startswith('/data/MEDIA'):
            img_url = 'https://korean.visitseoul.net' + img_url
        html += f'<img src="{img_url}" style="width:100%; border-radius:8px; margin-top:8px; margin-bottom:4px; max-height:150px; object-fit:cover;"><br>'
        
    html += f'<span class="address">주소: {address}</span><br>'
    
    if tagList and str(tagList) != 'nan':
        html += f'<span class="tag">{str(tagList)}</span>'
        
    html += '</div>'
    return html

def get_base_map(user_lat, user_lon):
    m = folium.Map(location=[user_lat, user_lon], zoom_start=14, tiles="CartoDB positron")
    # User marker
    folium.Marker(
        [user_lat, user_lon],
        popup="You are here",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    return m

def display_map_legend():
    # Legend style
    st.markdown("""
        <div style="padding: 20px; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 15px; margin-top: 20px; border: 1px solid rgba(255, 255, 255, 0.3); font-family: sans-serif; color: #000000;">
            <b style="font-size:15px; margin-right:20px; font-weight:700;">MAP LEGEND</b>
            <span style="margin-right:15px; font-weight:400;">🔴 다이소 (Daiso)</span>
            <span style="margin-right:15px; font-weight:400;">🟢 올리브영 (Olive Young)</span>
            <span style="margin-right:15px; font-weight:400;">🟡 관광지 (Attraction)</span>
            <span style="font-weight:400;">🔵 키오스크 (Kiosk)</span>
        </div>
    """, unsafe_allow_html=True)

def main():
    inject_custom_css()
    
    # Header Layout: Logo on Left, Menu on Right
    col_logo, col_menu = st.columns([1, 3])
    
    with col_logo:
        # K-Beauty MAP Logo (Hyperlink to reload app page)
        st.markdown(
            """
            <div style="margin-top: -2px; display: flex; align-items: center;">
                <a href="/" target="_self" 
                   style="text-decoration: none; color: #F93780; font-size: 22px; font-weight: 600; letter-spacing: -0.05em; line-height: 1;">
                   K-Beauty MAP
                </a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col_menu:
        # Top Horizontal Option Menu
        menu_options = ["HOME", "BEST ITEM", "FINDING THE STORE", "TOURIST ATTRACTION", "TAX REFUND"]
        
        selected_menu = option_menu(
            menu_title=None,
            options=menu_options,
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important", 
                    "background": "transparent", 
                    "margin-top": "0px", 
                    "margin-bottom": "60px",
                    "display": "flex",
                    "justify-content": "flex-end",
                },
                "icon": {"display": "none"},
                "nav": {
                    "justify-content": "flex-end",
                },
                "nav-item": {
                    "flex": "0 0 auto",
                    "margin": "0px",
                    "padding": "0px",
                },
                "nav-link": {
                    "font-size": "13px", 
                    "text-align": "right", 
                    "margin": "0px 15px", 
                    "padding": "10px 0px", 
                    "--hover-color": "transparent", 
                    "color": "#000000", 
                    "font-weight": "500", 
                    "letter-spacing": "-0.02em",
                    "background": "transparent",
                    "white-space": "nowrap",
                    "width": "auto"
                },
                "nav-link-selected": {
                    "background-color": "transparent", 
                    "color": "#F93780", 
                    "font-weight": "700", 
                    "text-decoration": "underline", 
                    "border": "none"
                },
            }
        )

    # User location fetch (applied globally for maps)
    location_data = None
    if selected_menu in ["FINDING THE STORE", "TOURIST ATTRACTION", "TAX REFUND"]:
        col1, col2 = st.columns([1, 10])
        with col1:
            location_data = streamlit_geolocation()
        with col2:
            st.markdown("<div style='margin-top:0.8rem; font-weight:600; font-family:sans-serif;'>MY LOCATION</div>", unsafe_allow_html=True)

    # Default fallback coords (Seoul City Hall)
    user_lat, user_lon = 37.5665, 126.9780
    if location_data and location_data.get('latitude') and location_data.get('longitude'):
        user_lat = location_data['latitude']
        user_lon = location_data['longitude']
        
    # --- Rendering Logic ---
    if selected_menu == "HOME":
        st.markdown("""
            <div style='min-height: 70vh; background-color: #FFFFFF; border-radius: 15px; border: 1px solid rgba(0,0,0,0.05); margin-top: 10px; display: flex; align-items: center; justify-content: center;'>
                <!-- Placeholder for future photos -->
            </div>
        """, unsafe_allow_html=True)

    elif selected_menu == "BEST ITEM":
        st.markdown("<h2 class='menu-heading'>BEST ITEM</h2>", unsafe_allow_html=True)
        
        tab_oy, tab_daiso = st.tabs(["OLIVE YOUNG", "DAISO"])
        
        # OLIVE YOUNG
        with tab_oy:
            df_oy = load_csv_data('best/oliveyoung_best_100.csv')
            if not df_oy.empty:
                cols = st.columns(5)
                for idx, row in df_oy.iterrows():
                    with cols[idx % 5]:
                        render_product_card(row, 'oliveyoung_best')
            else:
                st.warning("데이터를 불러올 수 없습니다.")
                    
        # DAISO
        with tab_daiso:
            df_daiso = load_csv_data('best/daiso_best_100.csv')
            if not df_daiso.empty:
                cols = st.columns(5)
                for idx, row in df_daiso.iterrows():
                    with cols[idx % 5]:
                        render_product_card(row, 'daiso_best')
            else:
                st.warning("데이터를 불러올 수 없습니다.")

    elif selected_menu == "FINDING THE STORE":
        st.markdown("<h2 class='menu-heading'>FINDING THE STORE</h2>", unsafe_allow_html=True)
        
        m = get_base_map(user_lat, user_lon)
        
        # Olive Young markers (Green #A6C302)
        df_oyshop = load_csv_data('stores/oliveyoung_stores.csv')
        oy_cluster = MarkerCluster(name="올리브영").add_to(m)
        for _, row in df_oyshop.iterrows():
            lat = row.get('latitude') if 'latitude' in row else row.get('위도')
            lon = row.get('longitude') if 'longitude' in row else row.get('경도')
            if pd.notna(lat) and pd.notna(lon):
                name = row.get('storeName') if 'storeName' in row else row.get('매장명', '')
                addr = row.get('address') if 'address' in row else row.get('주소', '')
                html = generate_popup_html('올리브영', name, addr)
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(html, max_width=250),
                    icon=folium.Icon(color="green", icon="shopping-cart", prefix="fa")
                ).add_to(oy_cluster)
                
        # Daiso markers (Red #E11937)
        df_daisoshop = load_csv_data('stores/daiso_stores.csv')
        daiso_cluster = MarkerCluster(name="다이소").add_to(m)
        for _, row in df_daisoshop.iterrows():
            if pd.notna(row.get('위도')) and pd.notna(row.get('경도')):
                html = generate_popup_html('다이소', row.get('매장명', ''), row.get('주소', ''))
                folium.Marker(
                    location=[row['위도'], row['경도']],
                    popup=folium.Popup(html, max_width=250),
                    icon=folium.Icon(color="red", icon="shopping-cart", prefix="fa")
                ).add_to(daiso_cluster)
                
        st_folium(m, center=[user_lat, user_lon], zoom=14, width=1200, height=600, returned_objects=[])
        display_map_legend()

    elif selected_menu == "TOURIST ATTRACTION":
        st.markdown("<h2 class='menu-heading'>TOURIST ATTRACTION</h2>", unsafe_allow_html=True)
        
        m_tour = get_base_map(user_lat, user_lon)
        
        # Tourist spots form tour_data.csv
        df_tour = load_csv_data('tout list/tour_data.csv')
        tour_cluster = MarkerCluster(name="관광지").add_to(m_tour)
        for _, row in df_tour.iterrows():
            if pd.notna(row.get('lat')) and pd.notna(row.get('lon')):
                html = generate_popup_html(
                    brand='관광지', 
                    name=row.get('postSj', '명소'), 
                    address=row.get('areaNm', '주소 미상'), 
                    tagList=row.get('tagList', ''),
                    imgUri=row.get('imageUri', '')
                )
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(html, max_width=250),
                    icon=folium.Icon(color="orange", icon="star")
                ).add_to(tour_cluster)

        st_folium(m_tour, center=[user_lat, user_lon], zoom=14, width=1200, height=600, returned_objects=[])
        display_map_legend()

    elif selected_menu == "TAX REFUND":
        st.markdown("<h2 class='menu-heading'>TAX REFUND KIOSK</h2>", unsafe_allow_html=True)
        
        m_tax = get_base_map(user_lat, user_lon)
        
        # Tax Kiosk
        df_kiosk = load_csv_data('stores/tax_kiosk_locations.csv')
        for _, row in df_kiosk.iterrows():
            lat_col, lon_col = None, None
            # Handle potential column name mismatches robustly
            if 'latitude' in row and 'longitude' in row:
                lat_col, lon_col = 'latitude', 'longitude'
            elif 'lat' in row and 'lon' in row:
                lat_col, lon_col = 'lat', 'lon'
                
            if lat_col and pd.notna(row.get(lat_col)) and pd.notna(row.get(lon_col)):
                name = row.get('name', 'Tax Refund Kiosk')
                addr = row.get('address', '')
                html = generate_popup_html('키오스크', name, addr)
                folium.Marker(
                    location=[row[lat_col], row[lon_col]],
                    popup=folium.Popup(html, max_width=250),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m_tax)

        st_folium(m_tax, center=[user_lat, user_lon], zoom=14, width=1200, height=600, returned_objects=[])
        display_map_legend()

if __name__ == "__main__":
    main()
