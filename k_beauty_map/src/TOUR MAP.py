    # --- TAB 4: MY TOUR MAP (Kakao & Realtime Congestion) ---
    elif selected_menu == "TOUR MAP":
        st.markdown("<h2 class='menu-heading'>MY PERSONA TOUR MAP</h2>", unsafe_allow_html=True)
        
        persona = st.session_state.get('user_persona', None)
        user_district = st.session_state.get('user_district', '전체')
        
        if not persona:
            st.warning("⚠️ HOME 탭에서 페르소나 진단을 먼저 진행해주세요! (Please complete the quiz first!)")
        
        display_name = PERSONA_INFO[persona][0] if persona else '전체 (진단 미완료)'
        st.sidebar.markdown(f"### 매핑 타겟: {display_name}")
        st.sidebar.markdown(f"### 추천 지역: {user_district}")        
        
        # 데이터가 있는 디렉토리 경로(TOUR_DATA_DIR)에서 데이터프레임을 불러옵니다
        df_tour = load_csv_data(os.path.join(TOUR_DATA_DIR, 'last_tour_final_mapped.csv'))
        if df_tour.empty:
            return st.error("관광지 매핑 데이터를 불러오지 못했습니다.")

        # 구 필터링 및 페르소나 필터링
        if user_district != '전체':
            df_curr = df_tour[df_tour['시/군/구'] == user_district]
            # 해당 구에 데이터가 부족하면 서울 전체에서 가져옴
            if len(df_curr) < 5:
                st.sidebar.info(f"💡 '{user_district}'에 적합한 추천지가 부족하여 서울 전체를 탐색합니다.")
            else:
                df_tour = df_curr
        if persona:
            df_tour = df_tour[df_tour['K뷰티_추천_페르소나'].astype(str).str.contains(persona, na=False)]
        
        df_tour = df_tour.sort_values(by='검색건수', ascending=False).head(50)
        
        # 실시간 데이터(서울시 혼잡도 API 연동) 조인
        map_data = []
        for _, row in df_tour.iterrows():
            if pd.notnull(row['lat']) and pd.notnull(row['lng']):
                cd = row.get('area_cd')
                cong = '정보없음'
                if pd.notnull(cd):
                    cdata = get_seoul_city_data(cd)
                    if "congestion_lvl" in cdata:
                        cong = cdata["congestion_lvl"]
                
                map_data.append({
                    'name': row['관광지명'],
                    'category': row['소분류 카테고리'],
                    'district': row['시/군/구'],
                    'lat': row['lat'],
                    'lng': row['lng'],
                    'congestion_lvl': cong,
                    'indoor': row.get('실내/실외 구분', '-'),
                    'age': row.get('추천 연령대', '-')
                })
        
        st.markdown(f"<p style='text-align:center;'>당신의 라이프스타일에 꼭 맞는 맞춤 관광지 <b>{len(map_data)}곳</b>을 선별했습니다.</p>", unsafe_allow_html=True)
        # render_kakao_map 함수가 외부에 선언되어 있어야 합니다. (현재 140~226번째 줄)
        render_kakao_map(map_data, center_lat=user_lat, center_lng=user_lon, level=6)

        # --- Section 4: 반나절 루트 제안 (The Actionable Itinerary) ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🗓️ Recommended Half-Day Itinerary")
        
        with st.expander("✨ 지금 바로 떠날 수 있는 '반나절 여행 코스' 보기 (Recommended Half-Day Course)", expanded=True):
            itinerary_data = {
                '중국': [
                    "📍 오전 11:00 - 명동역 인근 올리브영 타운 방문 (프리미엄 앰플 & 기기 쇼핑) <br> (11:00 AM - Visit Olive Young Town Myeongdong for premium care shopping)",
                    "📍 오후 13:00 - 더현대 서울 혹은 백화점 내 '무료 전시' 감상하며 인파 피하기 <br> (1:00 PM - Enjoy free exhibitions at The Hyundai Seoul or department stores)",
                    "📍 오후 16:00 - 한강 공원이 보이는 카페에서 럭셔리한 시티뷰 즐기기 <br> (4:00 PM - Enjoy luxury city view at a Han River view cafe)"
                ],
                '일본': [
                    "📍 오전 11:00 - 명동역 올리브영 방문 (텍스 리펀 챙기기 & 추천 마스크팩 구매) 🌿 <br> (11:00 AM - Visit Myeongdong Olive Young for tax refund & mask packs)",
                    "📍 오후 13:00 - 햇빛과 인파를 피할 수 있는 '근처 실내 전시관(여유 상태)'에서 문화생활 ☕ <br> (1:00 PM - Cultural life at a nearby quiet indoor gallery)",
                    "📍 오후 16:00 - 자극받은 피부를 쉬게 해주는 한적한 도심 공원 산책하기 🌳 <br> (4:00 PM - Rest your skin with a peaceful walk in a city park)"
                ],
                '대만': [
                    "📍 오전 11:00 - 트렌디한 시장(광장시장 등)에서 가벼운 로컬 푸드 체험 <br> (11:00 AM - Local food experience at trendy markets like Gwangjang Market)",
                    "📍 오후 13:00 - 쿨링이 필요한 피부를 위해 시원한 실내 팝업스토어 탐방 <br> (1:00 PM - Explore cool indoor pop-up stores for skin cooling)",
                    "📍 오후 16:00 - 모공 케어 아이템 장착 후 남산공원의 선선한 바람 쐬기 <br> (4:00 PM - Enjoy cool breeze at Namsan Park after pore care shopping)"
                ],
                '미국': [
                    "📍 오전 11:00 - 성수동 팝업스토어에서 가장 핫한 신상 글로우 제품 테스트 <br> (11:00 AM - Test hot new glow products at Seongsu-dong pop-ups)",
                    "📍 오후 13:00 - 힙한 대형 카페나 쇼핑 센터에서 숏폼 촬영하기 <br> (1:00 PM - Film short-form videos at hip grand cafes or malls)",
                    "📍 오후 16:00 - 액티비티가 어우러진 복합 문화 공간에서 에너지 충전 <br> (4:00 PM - Recharge energy at complex cultural spaces with activities)"
                ],
                '홍콩': [
                    "📍 오전 11:00 - 올인원 멀티밤 구매 후 동대문 복합 쇼핑 타워 정복 <br> (11:00 AM - Conquer Dongdaemun shopping towers with all-in-one balm)",
                    "📍 오후 13:00 - 짧은 시간 내에 고효율로 즐기는 공연 혹은 미디어 아트 관람 <br> (1:00 PM - Enjoy high-efficiency performances or media art)",
                    "📍 오후 16:00 - 환급 키오스크에서 세금 환급 후 청계천 밤도깨비 야시장 산책 <br> (4:00 PM - Walk along Cheonggyecheon after tax refund at a kiosk)"                ]
            }
            
            # 현재 페르소나에 맞는 루트 출력 (없으면 기본값 일반/공통 루트)
            selected_itinerary = itinerary_data.get(persona, itinerary_data['일본'])
            
            for step in selected_itinerary:
                st.markdown(f"**{step}**")
            
            st.markdown("---")
            st.info("💡 위 코스는 현재 지역의 실시간 혼잡도와 당신의 페르소나 성향을 고려하여 설계되었습니다. (This course is designed considering real-time congestion and your persona preference.)")
