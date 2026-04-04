    # --- TAB 1: HOME (PERSONA QUIZ) ---
    if selected_menu == "HOME (QUIZ)":
        st.markdown("<h2 class='menu-heading'>Find Your K-Beauty Persona & Area</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='quiz-card'>", unsafe_allow_html=True)
        with st.form("persona_quiz_form"):
            st.markdown("<div class='quiz-title'>Q1. K-뷰티 스킨케어 제품을 고를 때, 가장 중요하게 생각하는 것은? <br>(What is your priority when choosing K-Beauty skin care products?)</div>", unsafe_allow_html=True)
            q1 = st.radio("Purchase Priority", [
                "[A] 강력하고 확실한 프리미엄 기술력 (확실한 효과) / Premium technology (Clear results)",
                "[B] 매일 발라도 자극 없이 편안하고 순한 데일리 수분 / Daily moisture without irritation",
                "[C] 가볍고 산뜻하게 모공과 열감을 잡아주는 제품 / Pore & cooling with light finish",
                "[D] 성분이 과학적으로 증명되고 체계적인 기능과 루틴 / Scientifically proven ingredients & routine",
                "[E] 장벽부터 톤업까지 하나로 끝내는 고효율 멀티 솔루션 / High-efficiency multitasking care"
            ])
            
            st.markdown("<hr><div class='quiz-title'>Q2. 이상적인 서울 여행의 모습에 가장 가까운 것은? <br>(Which one best describes your ideal trip to Seoul?)</div>", unsafe_allow_html=True)
            q2 = st.radio("Travel Style", [
                "[A] 화려한 백화점에서 쇼핑하고, 럭셔리한 실내 스팟 즐기기 / Shopping & Luxury indoor spots",
                "[B] 트렌디한 시장이나 팝업스토어로 리프레시 투어 / Trendy markets & Pop-up stores",
                "[C] 고궁을 걷고 활기찬 액티비티 체험하기 / Palaces & Energetic activities",
                "[D] 전시관이나 자연 속에서 차분하게 시간 보내기 / Quiet galleries & Nature"
            ])
            
            st.markdown("<hr><div class='quiz-title'>Q3. K-뷰티 쇼핑으로 완성하고 싶은 당신의 피부 상태는? <br>(What is your desired skin condition after K-Beauty shopping?)</div>", unsafe_allow_html=True)
            q3 = st.radio("Skin Goal", [
                "[A] 늘어짐 없이 탱탱한 밀도를 가진 [고밀도 윤광 피부] / Firm and radiant [High-density glow]",
                "[B] 수분을 머금어 속부터 편안하고 맑은 [투명 물광 피부] / Clear and moisturized [Transparent water-glow]",
                "[C] 번들거림 없이 매끄럽고 모공이 없는 [클리어 보송 피부] / Matte and poreless [Clear matte skin]",
                "[D] 잡티 없이 튼튼하게 빛나는 [건강 브라이트닝 피부] / Healthy and blemish-free [Brightening skin]",
                "[E] 짧은 시간에 만들어내는 [단기 효율 톤업 피부] / Quick results [Instant tone-up]"
            ])

            st.markdown("<hr><div class='quiz-title'>Q4. 서울에서 현재 어디에 계시거나 방문하고 싶으신가요? <br>(Where are you currently staying or want to visit in Seoul?)</div>", unsafe_allow_html=True)
            # 참고: SEOUL_DISTRICTS 리스트가 상단 빈 공간에 먼저 선언되어 있어야 합니다. (현재 코드 237번째 줄)
            user_district_choice = st.selectbox("Preferred District (자치구 선택)", SEOUL_DISTRICTS)            
            submitted = st.form_submit_button("✨ 진단 결과 확인하기 (Show My Persona)")
            
        if submitted:
            st.session_state['user_district'] = user_district_choice.split(" (")[0]
            
            scores = {'중국':0, '일본':0, '대만':0, '미국':0, '홍콩':0}
            
            if "[A]" in q1: scores['중국'] += 2
            elif "[B]" in q1: scores['일본'] += 2
            elif "[C]" in q1: scores['대만'] += 2
            elif "[D]" in q1: scores['미국'] += 2
            elif "[E]" in q1: scores['홍콩'] += 2
            
            if "[A]" in q2: scores['중국'] += 1; scores['홍콩'] += 1
            elif "[B]" in q2: scores['대만'] += 1
            elif "[C]" in q2: scores['미국'] += 1
            elif "[D]" in q2: scores['일본'] += 1

            if "[A]" in q3: scores['중국'] += 1
            elif "[B]" in q3: scores['일본'] += 1
            elif "[C]" in q3: scores['대만'] += 1
            elif "[D]" in q3: scores['미국'] += 1
            elif "[E]" in q3: scores['홍콩'] += 1
            
            best_persona = max(scores, key=scores.get)
            st.session_state['user_persona'] = best_persona
            
            # 참고: PERSONA_INFO 딕셔너리가 상단 빈 공간에 먼저 선언되어 있어야 합니다. (현재 코드 229번째 줄)
            st.markdown(f"""
                <div class='result-card'>
                    <h1 style='color:#fff;'>당신의 K-뷰티 페르소나 (Your Persona)</h1>
                    <h2 style='font-size:35px; margin:20px 0;'>{PERSONA_INFO[best_persona][0]}</h2>
                    <p style='font-size:18px;'><i>"{PERSONA_INFO[best_persona][1]}"</i></p>
                    <p style="margin-top:20px; font-weight: 700;">방문 희망 지역: <span style='font-size: 1.2em;'>&#128205; {st.session_state.get('user_district', '전체')}</span><br>(Your Target Area)</p>
                    <p style="margin-top:20px;">상단 메뉴의 <b>[TOUR MAP]</b> 탭에서 당신의 성향과 위치에 맞는 관광지를 확인하세요!<br>(Check custom places in TOUR MAP tab!)</p>
                </div>
            """, unsafe_allow_html=True)
