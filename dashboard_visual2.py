import streamlit as st
import streamlit.components.v1 as components
import time
import json
import os
import math

# INSTELLINGEN
BESTANDSNAAM = 'sensor_data.json'
GELUID_STIL = 200     
GELUID_RUMOERIG = 600 

st.set_page_config(layout="wide", page_title="Heidelberglaan 15")
st.title("Heidelberglaan 15 Bureaubezetting")

# STATE MANAGEMENT
if 't1_display' not in st.session_state: st.session_state.t1_display = "Vrij"
if 't1_raw_last' not in st.session_state: st.session_state.t1_raw_last = "Vrij"
if 't1_change_time' not in st.session_state: st.session_state.t1_change_time = time.time()

if 't2_display' not in st.session_state: st.session_state.t2_display = "Vrij"
if 't2_raw_last' not in st.session_state: st.session_state.t2_raw_last = "Vrij"
if 't2_change_time' not in st.session_state: st.session_state.t2_change_time = time.time()

if 'sound_display_text' not in st.session_state: st.session_state.sound_display_text = "Stil"
if 'sound_level_1to10' not in st.session_state: st.session_state.sound_level_1to10 = 1
if 'last_sound_update' not in st.session_state: st.session_state.last_sound_update = time.time()

# DATA OPHALEN
def read_json_data():
    for i in range(5):
        if not os.path.exists(BESTANDSNAAM):
            time.sleep(0.1)
            continue
        try:
            with open(BESTANDSNAAM, 'r') as f:
                return json.load(f)
        except:
            time.sleep(0.05)
    return None

data = read_json_data()

if data is None:
    st.warning("Verbinding zoeken met sensoren...")
    time.sleep(1)
    st.rerun()

# Data veilig uitlezen
raw_t1 = data.get("tafel1", "VRIJ")
dist_1 = data.get("cm1", 0)
raw_t2 = data.get("tafel2", "VRIJ")
dist_2 = data.get("cm2", 0)
raw_sound = int(data.get("rawSound", 0))

# LOGICA (Status machine tafels)
def determine_display_state(current_display, last_raw, change_time, current_raw):
    if current_raw != last_raw:
        change_time = time.time()
        last_raw = current_raw
    
    time_diff = time.time() - change_time
    final_text = ""
    final_class = ""
    new_display = current_display

    # Scenario 1: Bezet -> Vrij
    if current_display == "Bezet" and current_raw == "VRIJ":
        if time_diff < 3:
            final_text = "BEZET"; final_class = "bezet knipperen"
        elif time_diff < 6:
            final_text = "EVEN WEG"; final_class = "koffie"
        else:
            new_display = "Vrij"; final_text = "VRIJ"; final_class = "vrij"
    
    # Scenario 2: Vrij -> Bezet
    elif current_display == "Vrij" and current_raw == "BEZET":
        if time_diff < 3:
            final_text = "VRIJ"; final_class = "vrij knipperen"
        else:
            new_display = "Bezet"; final_text = "BEZET"; final_class = "bezet"
            
    # Scenario 3: Blokkade
    elif current_raw == "BLOKKADE":
        if time_diff < 3:
            base_class = "bezet" if current_display == "Bezet" else "vrij"
            final_text = current_display.upper(); final_class = f"{base_class} knipperen"
        else:
            new_display = "Blokkade"; final_text = "BLOKKADE"; final_class = "blokkade"
            
    # Scenario 4: Stabiel
    else:
        if new_display == current_display: 
            if current_raw == "VRIJ": new_display = "Vrij"
            elif current_raw == "BEZET": new_display = "Bezet"
            elif current_raw == "BLOKKADE": new_display = "Blokkade"
        final_text = new_display.upper()
        if new_display == "Blokkade": final_text = "BLOKKADE"
        css_map = {"Vrij": "vrij", "Bezet": "bezet", "Blokkade": "blokkade"}
        final_class = css_map.get(new_display, "vrij")

    return new_display, last_raw, change_time, final_text, final_class

res_t1 = determine_display_state(st.session_state.t1_display, st.session_state.t1_raw_last, st.session_state.t1_change_time, raw_t1)
st.session_state.t1_display, st.session_state.t1_raw_last, st.session_state.t1_change_time, text_t1, class_t1 = res_t1

res_t2 = determine_display_state(st.session_state.t2_display, st.session_state.t2_raw_last, st.session_state.t2_change_time, raw_t2)
st.session_state.t2_display, st.session_state.t2_raw_last, st.session_state.t2_change_time, text_t2, class_t2 = res_t2

# GELUID LOGICA
current_time = time.time()
if current_time - st.session_state.last_sound_update > 2.0:
    if raw_sound < GELUID_STIL: 
        st.session_state.sound_display_text = "Stil"
    elif raw_sound < GELUID_RUMOERIG: 
        st.session_state.sound_display_text = "Rumoerig"
    else: 
        st.session_state.sound_display_text = "Luid"
    
    level = 1
    if raw_sound < GELUID_STIL:
        pct = raw_sound / GELUID_STIL
        level = 1 + int(pct * 2) 
    elif raw_sound < GELUID_RUMOERIG:
        pct = (raw_sound - GELUID_STIL) / (GELUID_RUMOERIG - GELUID_STIL)
        level = 4 + int(pct * 2) 
    else:
        level = 7 + int((raw_sound - GELUID_RUMOERIG) / 200) 
        if level > 10: level = 10
    
    st.session_state.sound_level_1to10 = level
    st.session_state.last_sound_update = current_time

# HTML GENERATOR
sound_blocks_html = ""
for i in range(10, 0, -1):
    color_class = ""
    if i >= 7: color_class = "block-red"      
    elif i >= 4: color_class = "block-orange" 
    else: color_class = "block-green"         
    
    state_class = "active" if st.session_state.sound_level_1to10 >= i else "inactive"
    sound_blocks_html += f'<div class="sound-block {color_class} {state_class}"></div>'

# Debug tekst voorbereiden
debug_text = f" DEBUG: Tafel 1 = {dist_1}cm ({raw_t1}) | Tafel 2 = {dist_2}cm ({raw_t2}) | Geluid = {raw_sound} (Level {st.session_state.sound_level_1to10})"

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        background-color: transparent;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .main-container {{
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-start; 
        gap: 80px; 
        padding-top: 20px;
        margin-bottom: 40px;
    }}
    .room-container {{
        display: flex;
        flex-direction: row;
        gap: 40px;
        align-items: center;
    }}
    .desk-group {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
    }}
    .desk-shape {{
        width: 160px;
        height: 120px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border: 2px solid rgba(255,255,255,0.2);
        transition: background-color 0.5s ease;
    }}
    .chair-shape {{
        width: 50px;
        height: 50px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: background-color 0.5s ease;
    }}
    .desk-label {{
        font-size: 12px; opacity: 0.9; text-transform: uppercase; margin-bottom: 5px;
    }}
    .sound-section {{
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    .sound-header {{ font-weight: bold; font-size: 18px; margin-bottom: 5px; }}
    .sound-status-text {{ font-size: 14px; color: #666; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
    .sound-meter {{
        display: flex;
        flex-direction: column;
        gap: 4px; 
        background-color: #eee;
        padding: 5px;
        border-radius: 4px;
    }}
    .sound-block {{ width: 60px; height: 20px; border-radius: 2px; transition: opacity 0.3s, background-color 0.3s; }}
    .block-green.active {{ background-color: #28a745; box-shadow: 0 0 5px #28a745; }}
    .block-orange.active {{ background-color: #fd7e14; box-shadow: 0 0 5px #fd7e14; }}
    .block-red.active {{ background-color: #dc3545; box-shadow: 0 0 5px #dc3545; }}
    .inactive {{ background-color: #d1d1d1; opacity: 0.4; }}
    
    .vrij {{ background-color: #28a745; }}
    .bezet {{ background-color: #dc3545; }}
    .koffie {{ background-color: #fd7e14; }}
    .blokkade {{ background-color: #007bff; }}
    
    @keyframes pulse {{ 0% {{opacity:1;}} 50% {{opacity:0.6;}} 100% {{opacity:1;}} }}
    .knipperen {{ animation: pulse 1s infinite; border: 3px solid white; }}
    
    /* DEBUG FOOTER STIJL */
    .debug-footer {{
        margin-top: 20px;
        padding-top: 10px;
        border-top: 1px solid #ccc;
        font-family: monospace;
        font-size: 12px;
        color: #555;
        width: 100%;
        text-align: center;
    }}
</style>
</head>
<body>
    <div class="main-container">
        <div class="room-container">
            <div class="desk-group">
                <div class="desk-shape {class_t1}">
                    <div class="desk-label">Tafel 1</div>
                    <div>{text_t1}</div>
                </div>
                <div class="chair-shape {class_t1}"></div>
            </div>
            <div class="desk-group">
                <div class="desk-shape {class_t2}">
                    <div class="desk-label">Tafel 2</div>
                    <div>{text_t2}</div>
                </div>
                <div class="chair-shape {class_t2}"></div>
            </div>
        </div>

        <div class="sound-section">
            <div class="sound-header">Geluidsniveau</div>
            <div class="sound-status-text">{st.session_state.sound_display_text}</div>
            <div class="sound-meter">
                {sound_blocks_html}
            </div>
        </div>
    </div>
    
    <div class="debug-footer">
        {debug_text}
    </div>

</body>
</html>
"""


components.html(html_content, height=650)

time.sleep(0.5)
st.rerun()
