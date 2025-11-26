"""
AI Property Description Generator - Enhanced UI/UX Version
Premium Quality with Groq Free API
Beautiful Modern Interface with Streamlit
"""

import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
from io import BytesIO
import time

# Page Configuration
st.set_page_config(
    page_title="AI Property Description Generator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS FOR ENHANCED UI ====================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Gradient Cards */
    .gradient-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: none;
    }
    
    .gradient-card-purple {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 1px solid #667eea30;
    }
    
    .gradient-card-green {
        background: linear-gradient(135deg, #11998e15 0%, #38ef7d15 100%);
        border: 1px solid #11998e30;
    }
    
    .gradient-card-orange {
        background: linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%);
        border: 1px solid #f093fb30;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #667eea;
    }
    
    .section-header h3 {
        color: #1a1a2e;
        font-weight: 700;
        margin: 0;
        font-size: 1.3rem;
    }
    
    .section-icon {
        font-size: 1.5rem;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-connected {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .status-disconnected {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    /* Version Badge */
    .version-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .style-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Feature Pills */
    .feature-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        color: #667eea;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid #667eea40;
        font-weight: 500;
    }
    
    /* Result Box */
    .result-box {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
        border: 2px solid #667eea30;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .result-title {
        color: #667eea;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .result-content {
        color: #1a1a2e;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Enhanced Description Box */
    .enhanced-box {
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
        border: 2px solid #38ef7d50;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Compare Boxes */
    .compare-original {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f350;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .compare-enhanced {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 2px solid #4caf5050;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        color: #1a1a2e;
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f5f7fa;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.2s;
    }
    
    .stCheckbox > label:hover {
        background: #667eea10;
        border-color: #667eea30;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #f0f4ff 100%);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea30, transparent);
        margin: 2rem 0;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-radius: 12px;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-radius: 12px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-radius: 12px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        border-radius: 12px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Quick Stats */
    .quick-stat {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .quick-stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .quick-stat-label {
        color: #666;
        font-size: 0.85rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ==================== AI GENERATION FUNCTIONS ====================
def test_groq_api(api_key):
    """Test Groq API connection"""
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key.strip()}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": "Say 'API is working!'"}],
                "temperature": 0.5,
                "max_tokens": 50
            },
            timeout=15
        )
        
        if response.status_code == 200:
            return True, "✅ API Connection Successful!"
        else:
            return False, f"Error {response.status_code}: {response.text[:200]}"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"


def generate_with_groq(property_data, api_key, retry_count=3, variation_seed=0):
    """Generate PREMIUM description using Groq API with variation support"""
    
    variation_prompts = [
        {
            'focus': 'lifestyle and experience',
            'tone': 'aspirational and emotional',
            'instruction': 'Focus on the lifestyle transformation and daily experiences this property offers.'
        },
        {
            'focus': 'investment value and practicality',
            'tone': 'professional and value-driven',
            'instruction': 'Emphasize the practical benefits, value for money, and smart investment aspects.'
        },
        {
            'focus': 'location benefits and connectivity',
            'tone': 'convenience-focused and modern',
            'instruction': 'Highlight the strategic location, connectivity advantages, and nearby conveniences.'
        },
        {
            'focus': 'comfort and luxury features',
            'tone': 'premium and sophisticated',
            'instruction': 'Emphasize the premium features, comfort elements, and luxurious living experience.'
        },
        {
            'focus': 'community and safety',
            'tone': 'warm and family-oriented',
            'instruction': 'Focus on the safe neighborhood, community aspects, and family-friendly environment.'
        }
    ]
    
    variation = variation_prompts[variation_seed % len(variation_prompts)]
    
    for attempt in range(retry_count):
        try:
            api_key = api_key.strip()
            
            bhk = property_data['bhk']
            prop_type = property_data['property_type'].title()
            locality = property_data['locality']
            city = property_data['city']
            district = property_data.get('district', '')
            state = property_data.get('state', '')
            pincode = property_data.get('pincode', '')
            area = property_data['area_sqft']
            rent = property_data['rent_amount']
            furnishing = property_data['furnishing_status']
            amenities = ', '.join(property_data['amenities']) if property_data['amenities'] else 'Standard amenities'
            tenants = property_data['preferred_tenants']
            deposit = property_data['deposit_amount']
            available = property_data['available_from']
            nearby = ', '.join(property_data.get('nearby_points', []))
            landmark = property_data.get('landmark', '')
            floor_no = property_data.get('floor_no', '')
            total_floors = property_data.get('total_floors', '')
            maintenance = property_data.get('maintenance', 0)
            
            rough_desc = property_data.get('rough_description', '').strip()
            rough_desc_section = ""
            if rough_desc:
                rough_desc_section = f"""

**Owner's Additional Notes/Description:**
"{rough_desc}"
(IMPORTANT: Please incorporate these owner-provided details naturally and prominently into the description!)
"""
            
            full_location = f"{locality}, {city}"
            if district:
                full_location += f", {district}"
            if state:
                full_location += f", {state}"
            if pincode:
                full_location += f" - {pincode}"
            
            location_details = full_location
            if landmark:
                location_details += f" (Near {landmark})"
            
            floor_info = ""
            if floor_no and total_floors:
                floor_info = f"\n- Floor: {floor_no} of {total_floors} floors"
            
            maintenance_info = ""
            if maintenance and maintenance > 0:
                maintenance_info = f"\n- Maintenance: ₹{maintenance}/month"

            prompt = f"""You are an expert real estate copywriter specializing in premium property listings.

Create a compelling rental property listing for:

**Property Details:**
- Type: {bhk} BHK {prop_type}
- Location: {location_details}
- Area: {area} square feet{floor_info}
- Monthly Rent: ₹{rent:,}
- Security Deposit: ₹{deposit:,}{maintenance_info}
- Furnishing: {furnishing} furnished
- Amenities: {amenities}
- Preferred Tenants: {tenants}
- Available From: {available}
- Nearby: {nearby if nearby else 'Various conveniences'}
{rough_desc_section}
**CREATIVE DIRECTION (Version #{variation_seed + 1}):**
- Primary Focus: {variation['focus']}
- Tone: {variation['tone']}
- Instruction: {variation['instruction']}

**Requirements:**
1. **Title**: Attention-grabbing, emotional title (8-12 words). DO NOT start with "Discover" or "Welcome".
2. **Teaser**: Compelling hook (15-20 words) with urgency
3. **Full Description**: Engaging 150-200 word description with lifestyle benefits
4. **Bullet Points**: 5 benefit-focused features
5. **SEO Keywords**: 5 search-optimized keywords
6. **Meta Title**: Under 60 chars
7. **Meta Description**: Under 160 chars with CTA

Return ONLY valid JSON:
{{
    "title": "captivating title here",
    "teaser_text": "compelling teaser here",
    "full_description": "detailed description here",
    "bullet_points": ["benefit 1", "benefit 2", "benefit 3", "benefit 4", "benefit 5"],
    "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "meta_title": "SEO meta title",
    "meta_description": "SEO meta description with CTA"
}}"""

            temperature = 0.8 + (variation_seed * 0.05)
            if temperature > 1.0:
                temperature = 0.8 + ((variation_seed % 3) * 0.05)

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are an expert real estate copywriter. Focus: {variation['focus']}. Tone: {variation['tone']}. Return only valid JSON."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": 2000,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                if content.startswith('```json'):
                    content = content.replace('```json', '').replace('```', '').strip()
                elif content.startswith('```'):
                    content = content.replace('```', '').strip()
                
                return json.loads(content)
            
            elif response.status_code == 429:
                if attempt < retry_count - 1:
                    time.sleep((attempt + 1) * 2)
                    continue
                return None
            else:
                return None
                
        except Exception as e:
            if attempt < retry_count - 1:
                time.sleep(2)
                continue
            return None
    
    return None


def generate_fallback(property_data):
    """Fallback template-based generation"""
    bhk = property_data['bhk']
    prop_type = property_data['property_type'].title()
    locality = property_data['locality']
    city = property_data['city']
    area = property_data['area_sqft']
    rent = property_data['rent_amount']
    furnishing = property_data['furnishing_status'].title()
    rough_desc = property_data.get('rough_description', '').strip()
    
    extra_info = f" {rough_desc}" if rough_desc else ""
    
    return {
        "title": f"Spacious {bhk} BHK {prop_type} for Rent in {locality}",
        "teaser_text": f"Well-maintained {bhk} BHK {prop_type} in prime {locality} location",
        "full_description": f"Looking for a comfortable home? This beautiful {bhk} BHK {prop_type} in {locality}, {city} is perfect for you. Spread across {area} sqft, this {furnishing} furnished property offers great value at ₹{rent:,}/month.{extra_info}",
        "bullet_points": [
            f"{bhk} BHK with {area} sqft area",
            f"{furnishing} furnished with modern fittings",
            f"Monthly rent: ₹{rent:,}",
            f"Preferred for: {property_data['preferred_tenants']}",
            f"Available from: {property_data['available_from']}"
        ],
        "seo_keywords": [f"{bhk} bhk {city}", f"{locality} rental", f"{prop_type} rent", f"flat {locality}", f"rent {city}"],
        "meta_title": f"{bhk} BHK {prop_type} for Rent in {locality}",
        "meta_description": f"Rent this {bhk} BHK in {locality}, {city}. {area} sqft, {furnishing}. ₹{rent:,}/month."
    }


def generate_description(property_data, api_provider, api_key=None, variation_seed=0):
    """Main generation function"""
    if api_provider == "Groq Premium (Free)" and api_key:
        result = generate_with_groq(property_data, api_key, variation_seed=variation_seed)
        if result:
            return result
    
    return generate_fallback(property_data)


def generate_enhanced_description(original_desc, property_data, style, length, api_key):
    """Generate enhanced version"""
    
    length_map = {
        "Medium (200-250 words)": "200-250 words",
        "Long (300-350 words)": "300-350 words", 
        "Extra Long (400-500 words)": "400-500 words"
    }
    target_length = length_map.get(length, "250-300 words")
    
    style_instructions = {
        "More Detailed & Elaborate": "Add more specific details about each feature and room descriptions.",
        "More Emotional & Persuasive": "Use emotional triggers and create vivid lifestyle imagery.",
        "More Professional & Formal": "Use sophisticated vocabulary and focus on specifications.",
        "Add Local Flavor & Culture": "Include references to local culture and neighborhood character.",
        "Focus on Investment Value": "Emphasize rental yield potential and location growth.",
        "Luxury & Premium Feel": "Use upscale vocabulary and emphasize exclusivity."
    }
    style_guide = style_instructions.get(style, "Make it more detailed.")
    
    location = f"{property_data['locality']}, {property_data['city']}"
    
    prompt = f"""Enhance this property description:

**ORIGINAL:**
{original_desc}

**PROPERTY:**
- {property_data['bhk']} BHK {property_data['property_type'].title()}
- Location: {location}
- Area: {property_data['area_sqft']} sq ft
- Rent: ₹{property_data['rent_amount']:,}/month

**STYLE:** {style_guide}
**LENGTH:** {target_length}

Return ONLY the enhanced description text, nothing else."""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key.strip()}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are an expert real estate copywriter. Return only the enhanced description."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 1500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            enhanced = result['choices'][0]['message']['content'].strip()
            
            for prefix in ["Here is", "Here's", "Enhanced description:", "Enhanced version:"]:
                if enhanced.lower().startswith(prefix.lower()):
                    enhanced = enhanced[len(prefix):].strip()
            
            return enhanced
        return None
            
    except Exception as e:
        return None


# ==================== MAIN APP ====================
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏠 AI Property Description Generator</h1>
        <p>Premium Quality Descriptions • FREE with Groq API • 5 Creative Styles • AI Enhancement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'generated_result' not in st.session_state:
        st.session_state.generated_result = None
    if 'property_data' not in st.session_state:
        st.session_state.property_data = None
    if 'generation_count' not in st.session_state:
        st.session_state.generation_count = 0
    if 'enhanced_description' not in st.session_state:
        st.session_state.enhanced_description = None
    if 'use_enhanced' not in st.session_state:
        st.session_state.use_enhanced = False
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="margin: 0;">⚙️ Configuration</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Provider
        api_provider = st.selectbox(
            "🤖 AI Provider",
            ["Groq Premium (Free)", "Template (No API)"],
            help="Groq Premium uses enhanced prompting for free!"
        )
        
        api_key = None
        if api_provider != "Template (No API)":
            st.markdown("""
            <div class="gradient-card gradient-card-green" style="padding: 1rem; margin: 1rem 0;">
                <p style="margin: 0; font-weight: 600;">🌟 PREMIUM Quality + FREE</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">Best of Both Worlds!</p>
            </div>
            """, unsafe_allow_html=True)
            
            api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
            
            st.markdown("[🔗 Get Free API Key](https://console.groq.com/keys)")
            
            if api_key:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🧪 Test", use_container_width=True):
                        with st.spinner("Testing..."):
                            success, message = test_groq_api(api_key)
                            if success:
                                st.session_state.api_connected = True
                                st.success("Connected!")
                            else:
                                st.session_state.api_connected = False
                                st.error("Failed")
                
                # Show connection status
                if st.session_state.api_connected:
                    st.markdown('<span class="status-badge status-connected">🟢 Connected</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-badge status-disconnected">🔴 Not Connected</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Features Info
        with st.expander("✨ Premium Features"):
            st.markdown("""
            - 🎨 **5 Creative Styles**
            - 🔄 **Unlimited Regeneration**
            - ✨ **AI Enhancement**
            - 📊 **Compare Versions**
            - 💾 **Multi-format Downloads**
            - 🎯 **SEO Optimization**
            """)
        
        with st.expander("🔄 Style Variations"):
            st.markdown("""
            1. 🌟 **Lifestyle & Experience**
            2. 💰 **Investment & Value**
            3. 📍 **Location & Connectivity**
            4. ✨ **Comfort & Luxury**
            5. 👨‍👩‍👧 **Community & Safety**
            """)
    
    # Main Content
    show_property_form(api_provider, api_key)


def show_property_form(api_provider, api_key):
    """Property Input Form with Enhanced UI"""
    
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📝</span>
        <h3>Property Details Entry Form</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Basic Details", "💰 Pricing & Availability", "✨ Features & Amenities"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            property_type = st.selectbox(
                "Property Type *",
                ["Flat", "Villa", "Independent House", "PG/Hostel", "Shop", "Office Space", "Studio Apartment", "Penthouse"]
            )
            
            bhk = st.selectbox(
                "BHK Configuration *",
                ["1 RK", "1 BHK", "2 BHK", "3 BHK", "4 BHK", "5 BHK", "5+ BHK", "Studio"]
            )
            
            area_sqft = st.number_input("Area (sq ft) *", min_value=100, max_value=50000, value=1000, step=50)
            
            furnishing = st.selectbox(
                "Furnishing Status *",
                ["Unfurnished", "Semi-Furnished", "Fully Furnished"]
            )
        
        with col2:
            state = st.selectbox(
                "State *",
                ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Telangana", "Gujarat", "Other"]
            )
            
            city = st.text_input("City *", value="Mumbai")
            locality = st.text_input("Locality *", value="Andheri West")
            landmark = st.text_input("Landmark", placeholder="Near XYZ Mall")
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                floor_no = st.number_input("Floor No.", min_value=0, max_value=100, value=5)
            with col_f2:
                total_floors = st.number_input("Total Floors", min_value=1, max_value=100, value=15)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            rent = st.number_input("Monthly Rent (₹) *", min_value=1000, max_value=10000000, value=25000, step=1000)
            deposit = st.number_input("Security Deposit (₹) *", min_value=0, max_value=50000000, value=50000, step=5000)
            maintenance = st.number_input("Maintenance (₹/month)", min_value=0, max_value=100000, value=2000, step=500)
        
        with col2:
            available = st.date_input("Available From *")
            preferred_tenants = st.multiselect(
                "Preferred Tenants *",
                ["Family", "Bachelors", "Students", "Company Lease", "Any"],
                default=["Family"]
            )
    
    with tab3:
        st.markdown("#### 🏢 Building Amenities")
        col1, col2, col3, col4 = st.columns(4)
        
        amenities = []
        
        with col1:
            if st.checkbox("🛗 Lift", value=True): amenities.append("Lift")
            if st.checkbox("🅿️ Parking", value=True): amenities.append("Parking")
            if st.checkbox("⚡ Power Backup"): amenities.append("Power Backup")
        
        with col2:
            if st.checkbox("🔒 Security", value=True): amenities.append("Security")
            if st.checkbox("📹 CCTV"): amenities.append("CCTV")
            if st.checkbox("🔥 Fire Safety"): amenities.append("Fire Safety")
        
        with col3:
            if st.checkbox("💪 Gym"): amenities.append("Gym")
            if st.checkbox("🏊 Pool"): amenities.append("Pool")
            if st.checkbox("🌳 Garden"): amenities.append("Garden")
        
        with col4:
            if st.checkbox("🏛️ Club House"): amenities.append("Club House")
            if st.checkbox("👶 Play Area"): amenities.append("Play Area")
            if st.checkbox("🧹 Maintenance Staff", value=True): amenities.append("Maintenance Staff")
        
        st.markdown("---")
        st.markdown("#### 🏠 Property Features")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.checkbox("🌅 Balcony", value=True): amenities.append("Balcony")
            if st.checkbox("🍳 Modular Kitchen"): amenities.append("Modular Kitchen")
        
        with col2:
            if st.checkbox("❄️ AC"): amenities.append("AC")
            if st.checkbox("🚿 Geyser"): amenities.append("Geyser")
        
        with col3:
            if st.checkbox("📶 WiFi"): amenities.append("WiFi")
            if st.checkbox("🚪 Wardrobe"): amenities.append("Wardrobe")
        
        with col4:
            if st.checkbox("📺 TV"): amenities.append("TV")
            if st.checkbox("🧺 Washing Machine"): amenities.append("Washing Machine")
        
        st.markdown("---")
        st.markdown("#### 📍 Nearby Points")
        col1, col2, col3 = st.columns(3)
        
        nearby_points = []
        
        with col1:
            if st.checkbox("🚇 Metro"): nearby_points.append("Metro Station")
            if st.checkbox("🚌 Bus Stop"): nearby_points.append("Bus Stop")
        
        with col2:
            if st.checkbox("🚆 Railway"): nearby_points.append("Railway Station")
            if st.checkbox("🏫 School"): nearby_points.append("School")
        
        with col3:
            if st.checkbox("🏥 Hospital"): nearby_points.append("Hospital")
            if st.checkbox("🛍️ Mall"): nearby_points.append("Mall")
        
        st.markdown("---")
        st.markdown("#### 📝 Additional Description")
        st.info("💡 Add unique selling points: corner flat, sea view, recently renovated, premium fittings...")
        rough_description = st.text_area(
            "Owner's Notes / Special Features",
            placeholder="Add any special features or unique selling points...",
            height=120
        )
    
    # Property Data
    property_data = {
        'property_type': property_type.lower(),
        'bhk': bhk,
        'area_sqft': area_sqft,
        'state': state,
        'city': city,
        'locality': locality,
        'landmark': landmark,
        'floor_no': floor_no,
        'total_floors': total_floors,
        'furnishing_status': furnishing.lower(),
        'rent_amount': rent,
        'deposit_amount': deposit,
        'maintenance': maintenance,
        'available_from': str(available),
        'preferred_tenants': ', '.join(preferred_tenants),
        'amenities': amenities,
        'nearby_points': nearby_points,
        'rough_description': rough_description
    }
    
    st.markdown("---")
    
    # Style hint
    if st.session_state.generation_count > 0:
        styles = ["🌟 Lifestyle", "💰 Investment", "📍 Location", "✨ Luxury", "👨‍👩‍👧 Community"]
        next_style = styles[st.session_state.generation_count % 5]
        st.info(f"🔄 Next style: **{next_style}**")
    
    # Buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        generate_clicked = st.button("🚀 Generate Premium Description", type="primary", use_container_width=True)
    
    with col2:
        regenerate_clicked = st.button("🔄 Regenerate", use_container_width=True, disabled=st.session_state.generated_result is None)
    
    with col3:
        clear_clicked = st.button("🗑️ Clear", use_container_width=True, disabled=st.session_state.generated_result is None)
    
    # Handle actions
    if clear_clicked:
        st.session_state.generated_result = None
        st.session_state.generation_count = 0
        st.session_state.enhanced_description = None
        st.session_state.use_enhanced = False
        st.rerun()
    
    if generate_clicked or regenerate_clicked:
        if not city or not locality:
            st.error("❌ Please fill City and Locality")
            return
        
        st.session_state.property_data = property_data
        st.session_state.enhanced_description = None
        st.session_state.use_enhanced = False
        
        if regenerate_clicked:
            st.session_state.generation_count += 1
        else:
            st.session_state.generation_count = 0
        
        with st.spinner("✨ Generating premium description..."):
            result = generate_description(property_data, api_provider, api_key, st.session_state.generation_count)
        
        if result:
            st.session_state.generated_result = result
            st.success("✅ Description generated!")
    
    # Display Results
    if st.session_state.generated_result:
        display_results(api_key)


def display_results(api_key):
    """Display generated results with enhanced UI"""
    result = st.session_state.generated_result
    property_data = st.session_state.property_data
    
    styles = ["🌟 Lifestyle", "💰 Investment", "📍 Location", "✨ Luxury", "👨‍👩‍👧 Community"]
    current_style = styles[st.session_state.generation_count % 5]
    
    st.markdown("---")
    
    # Version Info
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1.5rem;">
        <span class="version-badge">Version #{st.session_state.generation_count + 1}</span>
        <span class="style-badge">{current_style}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Title & Teaser
    st.markdown("""
    <div class="result-box">
        <div class="result-title">🏠 Property Title</div>
    </div>
    """, unsafe_allow_html=True)
    edited_title = st.text_input("Title", value=result['title'], label_visibility="collapsed")
    
    st.markdown("""
    <div class="result-box">
        <div class="result-title">✨ Teaser Line</div>
    </div>
    """, unsafe_allow_html=True)
    edited_teaser = st.text_input("Teaser", value=result['teaser_text'], label_visibility="collapsed")
    
    st.markdown("---")
    
    # Description Tabs
    st.markdown("### 📝 Full Description")
    
    desc_tab1, desc_tab2, desc_tab3 = st.tabs(["✏️ Edit", "🔄 AI Enhanced", "📊 Compare"])
    
    with desc_tab1:
        edited_description = st.text_area("Description", value=result['full_description'], height=200, label_visibility="collapsed")
        st.caption(f"📏 Word count: {len(edited_description.split())}")
    
    with desc_tab2:
        col1, col2 = st.columns(2)
        with col1:
            enhance_style = st.selectbox("Enhancement Style", [
                "More Detailed & Elaborate",
                "More Emotional & Persuasive",
                "More Professional & Formal",
                "Add Local Flavor & Culture",
                "Focus on Investment Value",
                "Luxury & Premium Feel"
            ])
        with col2:
            enhance_length = st.selectbox("Target Length", [
                "Medium (200-250 words)",
                "Long (300-350 words)",
                "Extra Long (400-500 words)"
            ])
        
        if st.button("✨ Generate Enhanced Version", type="primary"):
            if api_key:
                with st.spinner("🚀 Enhancing..."):
                    enhanced = generate_enhanced_description(
                        result['full_description'], property_data, enhance_style, enhance_length, api_key
                    )
                    if enhanced:
                        st.session_state.enhanced_description = enhanced
                        st.success("✅ Enhanced version ready!")
            else:
                st.error("Please enter API key")
        
        if st.session_state.enhanced_description:
            st.markdown("""<div class="enhanced-box">""", unsafe_allow_html=True)
            st.markdown("**Enhanced Description:**")
            enhanced_edited = st.text_area("Enhanced", value=st.session_state.enhanced_description, height=200, label_visibility="collapsed")
            st.session_state.enhanced_description = enhanced_edited
            st.caption(f"📏 Word count: {len(enhanced_edited.split())}")
            st.session_state.use_enhanced = st.checkbox("✅ Use in Downloads", value=st.session_state.use_enhanced)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with desc_tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="compare-original">', unsafe_allow_html=True)
            st.markdown("**🔵 Original:**")
            st.write(result['full_description'])
            st.caption(f"Words: {len(result['full_description'].split())}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="compare-enhanced">', unsafe_allow_html=True)
            st.markdown("**🟢 Enhanced:**")
            if st.session_state.enhanced_description:
                st.write(st.session_state.enhanced_description)
                st.caption(f"Words: {len(st.session_state.enhanced_description.split())}")
            else:
                st.info("Generate enhanced version first")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Final description
    final_description = st.session_state.enhanced_description if st.session_state.use_enhanced and st.session_state.enhanced_description else edited_description
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✨ Key Features")
        edited_bullets = []
        for i, point in enumerate(result['bullet_points'], 1):
            edited = st.text_input(f"Feature {i}", value=point, key=f"bullet_{i}")
            edited_bullets.append(edited)
    
    with col2:
        st.markdown("### 🔍 SEO")
        edited_keywords = st.text_input("Keywords", value=", ".join(result['seo_keywords']))
        edited_meta_title = st.text_input("Meta Title", value=result['meta_title'])
        edited_meta_desc = st.text_area("Meta Description", value=result['meta_description'], height=80)
    
    st.markdown("---")
    
    # Downloads
    st.markdown("### 💾 Download Options")
    
    edited_result = {
        'title': edited_title,
        'teaser_text': edited_teaser,
        'full_description': final_description,
        'bullet_points': edited_bullets,
        'seo_keywords': [k.strip() for k in edited_keywords.split(",")],
        'meta_title': edited_meta_title,
        'meta_description': edited_meta_desc
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_data = json.dumps({
            'property_details': property_data,
            'generated_content': edited_result,
            'version': st.session_state.generation_count + 1,
            'style': current_style
        }, indent=2)
        st.download_button("📄 Download JSON", json_data, f"property_v{st.session_state.generation_count + 1}.json", "application/json", use_container_width=True)
    
    with col2:
        text_content = f"""{edited_result['title']}
{edited_result['teaser_text']}

{edited_result['full_description']}

Features:
{chr(10).join(f"• {p}" for p in edited_result['bullet_points'])}

Keywords: {', '.join(edited_result['seo_keywords'])}
Meta Title: {edited_result['meta_title']}
Meta Description: {edited_result['meta_description']}

---
Version #{st.session_state.generation_count + 1} | {current_style}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
        st.download_button("📝 Download TXT", text_content, f"property_v{st.session_state.generation_count + 1}.txt", "text/plain", use_container_width=True)
    
    with col3:
        csv_data = pd.DataFrame([{
            'Title': edited_result['title'],
            'Description': edited_result['full_description'],
            'Features': ' | '.join(edited_result['bullet_points']),
            'Keywords': ', '.join(edited_result['seo_keywords']),
            'Version': st.session_state.generation_count + 1
        }])
        st.download_button("📊 Download CSV", csv_data.to_csv(index=False), f"property_v{st.session_state.generation_count + 1}.csv", "text/csv", use_container_width=True)


if __name__ == "__main__":
    main()
