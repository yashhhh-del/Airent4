"""
AI Property Description Generator - WITH REGENERATE FEATURE
Premium Quality with Groq Free API
Enhanced UI/UX Version
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
    page_title="🏠 AI Property Description Generator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #1f2937;
        border-left: 4px solid #667eea;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .premium-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #000;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .success-badge {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .info-badge {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8fafc;
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== INTERACTIVE PARSER ====================
class InteractiveParser:
    """Parser with interactive column mapping"""
    
    REQUIRED_FIELDS = {
        'property_type': 'Type of property (flat, villa, pg, shop, office)',
        'bhk': 'Number of bedrooms (2, 3, 1 BHK)',
        'area_sqft': 'Area in square feet',
        'city': 'City name (Mumbai, Delhi, etc)',
        'locality': 'Area/Locality name',
        'furnishing_status': 'Furnishing (unfurnished, semi, fully)',
        'rent_amount': 'Monthly rent amount',
        'deposit_amount': 'Security deposit amount',
        'available_from': 'Date when available',
        'preferred_tenants': 'Type of tenants (Family, Bachelor, etc)'
    }
    
    def __init__(self):
        self.errors = []
    
    def read_file(self, uploaded_file):
        """Read file without any changes"""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            self.errors.append(f"Error: {str(e)}")
            return None
    
    def apply_mapping(self, df, mapping):
        """Apply user's column mapping"""
        return df.rename(columns=mapping)
    
    def clean_and_process(self, df):
        """Clean and process data"""
        properties = []
        
        for idx, row in df.iterrows():
            try:
                # Parse amenities
                amenities = []
                if 'amenities' in row.index and pd.notna(row.get('amenities')):
                    amenities = [a.strip() for a in str(row['amenities']).split(',')]
                
                # Parse date
                available_from = row.get('available_from', datetime.now().date())
                if isinstance(available_from, str):
                    available_from = pd.to_datetime(available_from).date()
                elif isinstance(available_from, pd.Timestamp):
                    available_from = available_from.date()
                
                properties.append({
                    'property_type': str(row['property_type']).lower().strip(),
                    'bhk': str(row['bhk']).strip(),
                    'area_sqft': int(float(row['area_sqft'])),
                    'city': str(row['city']).strip(),
                    'locality': str(row['locality']).strip(),
                    'landmark': str(row.get('landmark', '')).strip(),
                    'floor_no': int(float(row['floor_no'])) if pd.notna(row.get('floor_no')) else None,
                    'total_floors': int(float(row['total_floors'])) if pd.notna(row.get('total_floors')) else None,
                    'furnishing_status': str(row['furnishing_status']).lower().strip(),
                    'rent_amount': float(row['rent_amount']),
                    'deposit_amount': float(row['deposit_amount']),
                    'available_from': str(available_from),
                    'preferred_tenants': str(row['preferred_tenants']).strip(),
                    'amenities': amenities,
                    'rough_description': str(row.get('rough_description', '')).strip(),
                })
            except Exception as e:
                self.errors.append(f"Row {idx+2}: {str(e)}")
        
        return properties


# ==================== AI GENERATION ====================
def test_groq_api(api_key):
    """Test Groq API connection with simple request"""
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
    
    # Variation prompts for different creative angles
    variation_prompts = [
        {
            'focus': 'lifestyle and experience',
            'tone': 'aspirational and emotional',
            'instruction': 'Focus on the lifestyle transformation and daily experiences this property offers. Paint a vivid picture of morning routines, evening relaxation, and the joy of living here.'
        },
        {
            'focus': 'investment value and practicality',
            'tone': 'professional and value-driven',
            'instruction': 'Emphasize the practical benefits, value for money, and smart investment aspects. Highlight cost savings, appreciation potential, and financial wisdom of this choice.'
        },
        {
            'focus': 'location benefits and connectivity',
            'tone': 'convenience-focused and modern',
            'instruction': 'Highlight the strategic location, connectivity advantages, and nearby conveniences. Focus on how this location saves time, offers accessibility, and enhances daily commute.'
        },
        {
            'focus': 'comfort and luxury features',
            'tone': 'premium and sophisticated',
            'instruction': 'Emphasize the premium features, comfort elements, and luxurious living experience. Use elegant language to describe the finer details and upscale amenities.'
        },
        {
            'focus': 'community and safety',
            'tone': 'warm and family-oriented',
            'instruction': 'Focus on the safe neighborhood, community aspects, and family-friendly environment. Highlight security features, neighbor relations, and child-friendly spaces.'
        }
    ]
    
    # Select variation based on seed
    variation = variation_prompts[variation_seed % len(variation_prompts)]
    
    for attempt in range(retry_count):
        try:
            # Clean API key
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
            water_supply = ', '.join(property_data.get('water_supply', []))
            water_availability = property_data.get('water_availability', '')
            
            # Include rough_description in prompt
            rough_desc = property_data.get('rough_description', '').strip()
            rough_desc_section = ""
            if rough_desc:
                rough_desc_section = f"""

**Owner's Additional Notes/Description:**
"{rough_desc}"
(IMPORTANT: Please incorporate these owner-provided details naturally and prominently into the description. These are unique selling points!)
"""
            
            # Build full location string
            full_location = f"{locality}, {city}"
            if district:
                full_location += f", {district}"
            if state:
                full_location += f", {state}"
            if pincode:
                full_location += f" - {pincode}"
            
            # Build location details with landmark
            location_details = full_location
            if landmark:
                location_details += f" (Near {landmark})"
            
            # Build floor info
            floor_info = ""
            if floor_no and total_floors:
                floor_info = f"\n- Floor: {floor_no} of {total_floors} floors"
            
            # Build maintenance info
            maintenance_info = ""
            if maintenance and maintenance > 0:
                maintenance_info = f"\n- Maintenance: ₹{maintenance}/month"
            
            # Build water supply info
            water_info = ""
            if water_supply:
                water_info = f"\n- Water Supply: {water_supply} ({water_availability})"

            prompt = f"""You are an expert real estate copywriter specializing in premium property listings that drive high engagement and conversions.

Create a compelling, professional rental property listing for:

**Property Details:**
- Type: {bhk} BHK {prop_type}
- Location: {location_details}
- Area: {area} square feet{floor_info}
- Monthly Rent: ₹{rent:,}
- Security Deposit: ₹{deposit:,}{maintenance_info}{water_info}
- Furnishing: {furnishing} furnished
- Amenities: {amenities}
- Preferred Tenants: {tenants}
- Available From: {available}
- Nearby: {nearby if nearby else 'Various conveniences'}
{rough_desc_section}
**CREATIVE DIRECTION FOR THIS VERSION (Version #{variation_seed + 1}):**
- Primary Focus: {variation['focus']}
- Tone: {variation['tone']}
- Special Instruction: {variation['instruction']}

**Requirements:**
1. **Title**: Create an attention-grabbing, emotional title (8-12 words) that highlights the property's unique value proposition and creates desire. Make it DIFFERENT from generic titles. DO NOT start with "Discover" or "Welcome".
2. **Teaser**: Write a compelling hook (15-20 words) that creates urgency and paints a lifestyle picture
3. **Full Description**: Craft a detailed, engaging description (150-200 words) that:
   - Paints a vivid picture of living there
   - Highlights lifestyle benefits, not just features
   - Uses emotional, sensory language
   - Emphasizes location advantages and convenience
   - Creates FOMO (fear of missing out)
   - Focuses on the experience and feelings
   - Follows the creative direction provided above
   - INCORPORATES any owner notes/rough description provided
4. **Bullet Points**: 5 compelling features written as BENEFITS (not just specs). Focus on what the tenant gains. Make them unique and specific.
5. **SEO Keywords**: 5 highly relevant, search-optimized keywords that people actually search for
6. **Meta Title**: SEO-optimized title (under 60 chars) with primary keyword
7. **Meta Description**: Compelling SEO description (under 160 chars) with call-to-action

**Tone**: {variation['tone']}. Write like you're selling a dream lifestyle, not just a property.

**IMPORTANT - MAKE IT UNIQUE:**
- Use varied vocabulary and expressions
- Try different angles and perspectives  
- Create original metaphors and descriptions
- Avoid repetitive patterns
- Each regeneration should feel fresh and different

Return ONLY valid JSON (no markdown, no ```json):
{{
    "title": "your captivating title here",
    "teaser_text": "your compelling teaser here",
    "full_description": "your detailed engaging description here",
    "bullet_points": ["lifestyle benefit 1", "lifestyle benefit 2", "lifestyle benefit 3", "lifestyle benefit 4", "lifestyle benefit 5"],
    "seo_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "meta_title": "your SEO meta title here",
    "meta_description": "your SEO meta description with CTA here"
}}"""

            # Adjust temperature based on variation for more creativity
            temperature = 0.8 + (variation_seed * 0.05)
            if temperature > 1.0:
                temperature = 0.8 + ((variation_seed % 3) * 0.05)

            # Make API request
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
                            "content": f"You are an expert real estate copywriter creating premium, emotionally engaging property listings. For this generation (Version #{variation_seed + 1}), your focus is on {variation['focus']} with a {variation['tone']} tone. Write compelling, benefit-focused content that sells lifestyle and experience, not just features. Be creative and avoid repetitive patterns. If owner notes are provided, incorporate them prominently. Always respond with valid JSON only, no markdown formatting."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": 2000,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Clean markdown formatting if present
                if content.startswith('```json'):
                    content = content.replace('```json', '').replace('```', '').strip()
                elif content.startswith('```'):
                    content = content.replace('```', '').strip()
                
                # Parse JSON
                parsed = json.loads(content)
                return parsed
            
            # Handle errors
            elif response.status_code == 429:
                if attempt < retry_count - 1:
                    wait_time = (attempt + 1) * 2
                    st.warning(f"⏳ Rate limit hit. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error("❌ Rate limit exceeded. Please wait a minute and try again.")
                    return None
            
            elif response.status_code == 401:
                st.error("❌ Invalid API Key")
                st.info("🔑 Get a new API key from: https://console.groq.com/keys")
                return None
            
            elif response.status_code == 400:
                error_data = response.json()
                st.error(f"❌ Bad Request: {error_data}")
                return None
            
            else:
                st.error(f"❌ API Error {response.status_code}")
                with st.expander("🔍 Error Details"):
                    st.code(response.text)
                return None
                
        except requests.exceptions.Timeout:
            if attempt < retry_count - 1:
                st.warning(f"⏳ Timeout. Retrying... (Attempt {attempt + 2}/{retry_count})")
                time.sleep(2)
                continue
            else:
                st.error("❌ Request timeout after multiple attempts")
                return None
        
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON response from Groq")
            with st.expander("🔍 Response Details"):
                st.text(content if 'content' in locals() else "No content received")
            return None
        
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
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
    
    # Include rough description in fallback if provided
    extra_info = ""
    if rough_desc:
        extra_info = f" {rough_desc}"
    
    return {
        "title": f"Spacious {bhk} BHK {prop_type} for Rent in {locality}",
        "teaser_text": f"Well-maintained {bhk} BHK {prop_type} in prime {locality} location",
        "full_description": f"Looking for a comfortable home? This beautiful {bhk} BHK {prop_type} in {locality}, {city} is perfect for you. Spread across {area} sqft, this {furnishing} furnished property offers great value at ₹{rent:,}/month. Located in a well-connected area with easy access to essential amenities.{extra_info}",
        "bullet_points": [
            f"{bhk} BHK configuration with {area} sqft carpet area",
            f"{furnishing} furnished with modern fittings",
            f"Monthly rent: ₹{rent:,} | Deposit: ₹{property_data['deposit_amount']:,}",
            f"Preferred for: {property_data['preferred_tenants']}",
            f"Available from: {property_data['available_from']}"
        ],
        "seo_keywords": [
            f"{bhk} bhk {city}",
            f"{locality} rental",
            f"{prop_type} for rent {city}",
            f"{furnishing} flat {locality}",
            f"rent {bhk}bhk {city}"
        ],
        "meta_title": f"{bhk} BHK {prop_type} for Rent in {locality}, {city}",
        "meta_description": f"Rent this spacious {bhk} BHK {prop_type} in {locality}, {city}. {area} sqft, {furnishing} furnished. ₹{rent:,}/month. Available now!"
    }


def generate_description(property_data, api_provider, api_key=None, variation_seed=0):
    """Main generation function with multiple providers and variation support"""
    if api_provider == "Groq Premium (Free)" and api_key:
        result = generate_with_groq(property_data, api_key, variation_seed=variation_seed)
        if result:
            return result
    
    # Fallback to template
    st.info("ℹ️ Using template-based generation")
    return generate_fallback(property_data)


def generate_enhanced_description(original_desc, property_data, style, length, api_key):
    """Generate an enhanced version of the description using AI"""
    
    # Map length selection to word count
    length_map = {
        "Medium (200-250 words)": "200-250 words",
        "Long (300-350 words)": "300-350 words", 
        "Extra Long (400-500 words)": "400-500 words"
    }
    target_length = length_map.get(length, "250-300 words")
    
    # Map style to instructions
    style_instructions = {
        "More Detailed & Elaborate": "Add more specific details about each feature, room descriptions, and practical benefits. Include sensory details about spaces, lighting, and ambiance.",
        "More Emotional & Persuasive": "Use emotional triggers, create vivid lifestyle imagery, add aspirational language. Make the reader feel excited and create urgency.",
        "More Professional & Formal": "Use sophisticated vocabulary, focus on specifications and value proposition. Suitable for corporate tenants and professionals.",
        "Add Local Flavor & Culture": "Include references to local culture, nearby famous spots, local food scenes, and neighborhood character. Make it feel authentic to the location.",
        "Focus on Investment Value": "Emphasize rental yield potential, appreciation prospects, location growth, infrastructure development, and smart financial decision aspects.",
        "Luxury & Premium Feel": "Use upscale vocabulary, emphasize exclusivity, premium finishes, and sophisticated lifestyle. Make it feel like a luxury listing."
    }
    style_guide = style_instructions.get(style, "Make it more detailed and engaging.")
    
    # Build location string
    location = f"{property_data['locality']}, {property_data['city']}"
    if property_data.get('district'):
        location += f", {property_data['district']}"
    
    prompt = f"""You are an expert real estate copywriter. Enhance the following property description.

**ORIGINAL DESCRIPTION:**
{original_desc}

**PROPERTY QUICK INFO:**
- {property_data['bhk']} BHK {property_data['property_type'].title()}
- Location: {location}
- Area: {property_data['area_sqft']} sq ft
- Rent: ₹{property_data['rent_amount']:,}/month
- Furnishing: {property_data['furnishing_status']}
- Amenities: {', '.join(property_data.get('amenities', []))}

**ENHANCEMENT STYLE:** {style}
**STYLE INSTRUCTIONS:** {style_guide}

**TARGET LENGTH:** {target_length}

**REQUIREMENTS:**
1. Keep all factual information accurate
2. Maintain the core message but enhance the presentation
3. Add more vivid descriptions and emotional appeal
4. Include specific benefits for the target tenant
5. Create a stronger call-to-action
6. Make it unique and memorable
7. Follow the style instructions closely

**IMPORTANT:** 
- Return ONLY the enhanced description text
- Do NOT include any headers, labels, or formatting
- Do NOT start with "Here is" or similar phrases
- Just write the enhanced property description directly
"""

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
                    {
                        "role": "system",
                        "content": f"You are an expert real estate copywriter specializing in {style.lower()}. Enhance property descriptions to be more compelling while keeping facts accurate. Return only the enhanced description text, nothing else."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8,
                "max_tokens": 1500,
                "top_p": 0.9
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            enhanced = result['choices'][0]['message']['content'].strip()
            
            # Clean up any unwanted prefixes
            unwanted_prefixes = [
                "Here is the enhanced description:",
                "Here's the enhanced version:",
                "Enhanced description:",
                "Enhanced version:",
                "Here is",
                "Here's"
            ]
            for prefix in unwanted_prefixes:
                if enhanced.lower().startswith(prefix.lower()):
                    enhanced = enhanced[len(prefix):].strip()
            
            return enhanced
        else:
            st.error(f"❌ API Error: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# ==================== MAIN APP ====================
def main():
    # Header with gradient
    st.markdown('<h1 class="main-header">🏠 AI Property Description Generator</h1>', unsafe_allow_html=True)
    
    # Hero section
    col_hero1, col_hero2, col_hero3 = st.columns([2, 1, 1])
    with col_hero1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white;">
            <h3 style="color: white; margin: 0;">✨ Create Compelling Property Listings</h3>
            <p style="color: white; margin: 0.5rem 0 0 0; opacity: 0.9;">
            Premium AI-powered descriptions that attract quality tenants and maximize engagement
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_hero2:
        st.metric("🎯 Premium Quality", "AI Powered", delta="Free")
    
    with col_hero3:
        st.metric("🔄 Multiple Styles", "5 Variations", delta="Regenerate")
    
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
    if 'enhanced_edit_mode' not in st.session_state:
        st.session_state.enhanced_edit_mode = False
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 8px; color: white; margin-bottom: 1rem;">
            <h4 style="color: white; margin: 0;">⚙️ Configuration</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Provider Selection
        api_provider = st.selectbox(
            "Select AI Provider",
            ["Groq Premium (Free)", "Template (No API)"],
            help="Groq Premium uses enhanced prompting for free premium quality!",
            key="api_provider_select"
        )
        
        # API Key Input
        api_key = None
        if api_provider != "Template (No API)":
            st.markdown('<div class="premium-badge">PREMIUM</div>', unsafe_allow_html=True)
            st.success("🌟 PREMIUM Quality + FREE - Best of Both Worlds!")
            st.info("🆓 Get free Groq API key from: https://console.groq.com/keys")
            api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...", key="groq_api_key")
            
            # Test API button
            if api_key:
                col_test1, col_test2 = st.columns([3, 1])
                with col_test1:
                    if st.button("🧪 Test API Connection", key="test_api_btn", use_container_width=True):
                        with st.spinner("Testing connection..."):
                            success, message = test_groq_api(api_key)
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
        
        st.divider()
        
        # Quick Stats
        if st.session_state.generated_result:
            st.markdown("### 📊 Generation Stats")
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Versions", st.session_state.generation_count + 1)
            with col_stat2:
                style_names = ["Lifestyle", "Investment", "Location", "Luxury", "Community"]
                current_style = style_names[st.session_state.generation_count % 5]
                st.metric("Current Style", current_style)
        
        # Feature Info
        with st.expander("🎯 About Features", expanded=True):
            st.markdown("""
            **✨ Premium Features:**
            - 🎨 5 Creative Writing Styles
            - 🔄 Smart Regeneration
            - 🚀 AI Enhancement
            - 📊 SEO Optimization
            - 💾 Multiple Export Formats
            
            **🔄 Regenerate Styles:**
            1. 🌟 Lifestyle & Experience
            2. 💰 Investment & Value  
            3. 📍 Location & Connectivity
            4. ✨ Comfort & Luxury
            5. 👨‍👩‍👧 Community & Safety
            """)
        
        st.divider()
        
        # Quick Actions
        if st.session_state.generated_result:
            st.markdown("### ⚡ Quick Actions")
            if st.button("🗑️ Clear All Results", use_container_width=True):
                st.session_state.generated_result = None
                st.session_state.generation_count = 0
                st.session_state.enhanced_description = None
                st.session_state.use_enhanced = False
                st.session_state.enhanced_edit_mode = False
                st.rerun()
    
    # Main content area
    show_single_property(api_provider, api_key)


def show_single_property(api_provider, api_key):
    """Comprehensive Property Input Module with Enhanced UI"""
    
    # Progress tracker
    if st.session_state.generated_result is None:
        st.markdown("### 📋 Property Details Form")
        st.caption("Fill in all details to generate premium property description")
        
        # Progress steps
        current_step = 1
        total_steps = 3
        progress = current_step / total_steps
        
        col_prog1, col_prog2, col_prog3 = st.columns(3)
        with col_prog1:
            st.markdown(f"**{current_step}. Basic Details**")
        with col_prog2:
            st.markdown(f"**{current_step + 1}. Pricing**")
        with col_prog3:
            st.markdown(f"**{current_step + 2}. Features**")
        
        st.progress(progress)
    
    # Create tabs with icons
    tab1, tab2, tab3 = st.tabs(["🏠 Basic Details", "💰 Pricing & Availability", "✨ Features & Amenities"])
    
    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">Basic Property Information</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_type = st.selectbox(
                "Property Type *",
                ["Flat", "Villa", "Independent House", "PG/Hostel", "Shop", "Office Space", 
                 "Warehouse", "Land/Plot", "Studio Apartment", "Penthouse"],
                help="Select the type of property",
                key="prop_type_select"
            )
            
            bhk = st.selectbox(
                "BHK Configuration / Rooms *",
                ["1 RK", "1 BHK", "2 BHK", "3 BHK", "4 BHK", "5 BHK", "5+ BHK", 
                 "Studio", "Other"],
                help="Number of bedrooms, hall, and kitchen",
                key="bhk_select"
            )
            
            area_unit = st.radio("Area Unit", ["sq ft", "sq m"], horizontal=True, key="area_unit_radio")
            area_sqft = st.number_input(
                f"Built-up Area ({area_unit}) *",
                min_value=100,
                max_value=50000,
                value=1000,
                step=50,
                help="Total built-up area of the property",
                key="area_input"
            )
            
            furnishing = st.selectbox(
                "Furnishing Status *",
                ["Unfurnished", "Semi-Furnished", "Fully Furnished"],
                help="Current furnishing level of the property",
                key="furnishing_select"
            )
        
        with col2:
            # State Selection
            state = st.selectbox(
                "State *",
                ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Telangana", "Gujarat", 
                 "Uttar Pradesh", "West Bengal", "Rajasthan", "Madhya Pradesh", "Kerala",
                 "Punjab", "Haryana", "Bihar", "Odisha", "Andhra Pradesh", "Jharkhand",
                 "Assam", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh", "Goa", "Other"],
                help="State where property is located",
                key="state_input"
            )
            
            col_loc1, col_loc2 = st.columns(2)
            with col_loc1:
                district = st.text_input(
                    "District *",
                    value="Mumbai Suburban",
                    help="District name",
                    key="district_input"
                )
            
            with col_loc2:
                city = st.text_input(
                    "City/Town *",
                    value="Mumbai",
                    help="City or town name",
                    key="city_input"
                )
            
            col_loc3, col_loc4 = st.columns(2)
            with col_loc3:
                locality = st.text_input(
                    "Area/Locality *",
                    value="Andheri West",
                    help="Specific area or locality name",
                    key="locality_input"
                )
            
            with col_loc4:
                pincode = st.text_input(
                    "Pincode",
                    placeholder="e.g., 400053",
                    help="6-digit PIN code",
                    key="pincode_input"
                )
            
            landmark = st.text_input(
                "Landmark (Optional)",
                placeholder="e.g., Near XYZ Mall, Opposite ABC Hospital",
                help="Prominent landmark near the property",
                key="landmark_input"
            )
            
            col_floor1, col_floor2 = st.columns(2)
            with col_floor1:
                floor_no = st.number_input(
                    "Floor Number",
                    min_value=0,
                    max_value=100,
                    value=5,
                    help="Floor on which property is located (0 for ground)",
                    key="floor_no_input"
                )
            
            with col_floor2:
                total_floors = st.number_input(
                    "Total Floors",
                    min_value=1,
                    max_value=100,
                    value=10,
                    help="Total floors in the building",
                    key="total_floors_input"
                )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">Pricing & Availability Details</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            rent = st.number_input(
                "Monthly Rent (₹) *",
                min_value=1000,
                max_value=10000000,
                value=25000,
                step=1000,
                help="Monthly rental amount",
                key="rent_input"
            )
            
            deposit = st.number_input(
                "Security Deposit (₹) *",
                min_value=0,
                max_value=50000000,
                value=50000,
                step=5000,
                help="Refundable security deposit",
                key="deposit_input"
            )
            
            maintenance = st.number_input(
                "Maintenance (₹/month)",
                min_value=0,
                max_value=100000,
                value=2000,
                step=500,
                help="Monthly maintenance charges (if applicable)",
                key="maintenance_input"
            )
        
        with col2:
            available = st.date_input(
                "Available From *",
                help="Date when property will be available for move-in",
                key="available_date"
            )
            
            preferred_tenants = st.multiselect(
                "Preferred Tenants *",
                ["Family", "Bachelors", "Students", "Company Lease", "Any"],
                default=["Family"],
                help="Type of tenants preferred (can select multiple)",
                key="tenants_multiselect"
            )
            
            negotiable = st.checkbox("Rent Negotiable", value=False, key="negotiable_check")
            parking_charges = st.number_input(
                "Parking Charges (₹/month)",
                min_value=0,
                max_value=10000,
                value=0,
                help="Additional parking charges if any",
                key="parking_input"
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">Features & Amenities</h3>', unsafe_allow_html=True)
        
        st.markdown("#### 🏢 Building Amenities")
        col1, col2, col3, col4 = st.columns(4)
        
        amenities = []
        
        with col1:
            st.markdown("**Essential Amenities**")
            if st.checkbox("Lift/Elevator", value=True, key="amenity_lift"):
                amenities.append("Lift")
            if st.checkbox("Parking", value=True, key="amenity_parking"):
                amenities.append("Parking")
            if st.checkbox("Power Backup", value=False, key="amenity_power"):
                amenities.append("Power Backup")
            if st.checkbox("Security", value=True, key="amenity_security"):
                amenities.append("Security")
        
        with col2:
            st.markdown("**Safety & Security**")
            if st.checkbox("CCTV Surveillance", value=False, key="amenity_cctv"):
                amenities.append("CCTV")
            if st.checkbox("Intercom", value=False, key="amenity_intercom"):
                amenities.append("Intercom")
            if st.checkbox("Fire Safety", value=False, key="amenity_fire"):
                amenities.append("Fire Safety")
            if st.checkbox("Waste Disposal", value=True, key="amenity_waste"):
                amenities.append("Waste Disposal")
        
        with col3:
            st.markdown("**Lifestyle Amenities**")
            if st.checkbox("Gym/Fitness Center", value=False, key="amenity_gym"):
                amenities.append("Gym")
            if st.checkbox("Swimming Pool", value=False, key="amenity_pool"):
                amenities.append("Pool")
            if st.checkbox("Garden/Park", value=False, key="amenity_garden"):
                amenities.append("Garden")
            if st.checkbox("Children's Play Area", value=False, key="amenity_play"):
                amenities.append("Play Area")
        
        with col4:
            st.markdown("**Community Amenities**")
            if st.checkbox("Club House", value=False, key="amenity_club"):
                amenities.append("Club House")
            if st.checkbox("Visitor Parking", value=False, key="amenity_visitor"):
                amenities.append("Visitor Parking")
            if st.checkbox("Maintenance Staff", value=True, key="amenity_maintenance"):
                amenities.append("Maintenance Staff")
        
        st.divider()
        
        # Water Supply Section
        st.markdown("#### 💧 Water Supply Details")
        col_water1, col_water2 = st.columns(2)
        
        water_sources = []
        with col_water1:
            water_supply_type = st.multiselect(
                "Water Supply Source *",
                ["Corporation/Municipal", "Borewell/Tubewell", "Tanker", "Ground Water", 
                 "Rain Water Harvesting", "Water Purifier Available"],
                default=["Corporation/Municipal"],
                help="Select all applicable water sources",
                key="water_supply_type"
            )
            water_sources.extend(water_supply_type)
        
        with col_water2:
            water_availability = st.selectbox(
                "Water Availability",
                ["24/7 Available", "Morning & Evening", "Once a Day", "Twice a Day", "As per Schedule"],
                help="When is water available",
                key="water_availability"
            )
            if water_availability != "24/7 Available":
                amenities.append(f"Water: {water_availability}")
            else:
                amenities.append("24/7 Water Supply")
        
        # Add water sources to amenities
        for source in water_sources:
            if source not in ["Corporation/Municipal"]:  # Don't add common one
                amenities.append(source)
        
        st.divider()
        
        st.markdown("#### 🏠 Property Features")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Living Space**")
            if st.checkbox("Balcony", value=True, key="feature_balcony"):
                amenities.append("Balcony")
            if st.checkbox("Modular Kitchen", value=False, key="feature_kitchen"):
                amenities.append("Modular Kitchen")
        
        with col2:
            st.markdown("**Furniture**")
            if st.checkbox("Wardrobe", value=False, key="feature_wardrobe"):
                amenities.append("Wardrobe")
            if st.checkbox("Sofa", value=False, key="feature_sofa"):
                amenities.append("Sofa")
            if st.checkbox("Bed", value=False, key="feature_bed"):
                amenities.append("Bed")
        
        with col3:
            st.markdown("**Appliances**")
            if st.checkbox("AC", value=False, key="feature_ac"):
                amenities.append("Air Conditioning")
            if st.checkbox("Geyser", value=False, key="feature_geyser"):
                amenities.append("Geyser")
            if st.checkbox("Washing Machine", value=False, key="feature_washing"):
                amenities.append("Washing Machine")
        
        with col4:
            st.markdown("**Electronics**")
            if st.checkbox("WiFi/Internet", value=False, key="feature_wifi"):
                amenities.append("Internet")
            if st.checkbox("TV", value=False, key="feature_tv"):
                amenities.append("TV")
            if st.checkbox("Fridge", value=False, key="feature_fridge"):
                amenities.append("Refrigerator")
        
        st.divider()
        
        st.markdown("#### 📍 Nearby Points of Interest")
        col1, col2 = st.columns(2)
        
        nearby_points = []
        
        with col1:
            st.markdown("**Transportation**")
            if st.checkbox("Metro Station", value=False, key="nearby_metro"):
                distance = st.text_input("Distance from Metro", placeholder="e.g., 500m", key="metro_dist")
                nearby_points.append(f"Metro Station ({distance})" if distance else "Metro Station")
            
            if st.checkbox("Bus Stop", value=False, key="nearby_bus"):
                distance = st.text_input("Distance from Bus Stop", placeholder="e.g., 200m", key="bus_dist")
                nearby_points.append(f"Bus Stop ({distance})" if distance else "Bus Stop")
            
            if st.checkbox("Railway Station", value=False, key="nearby_railway"):
                distance = st.text_input("Distance from Railway", placeholder="e.g., 2km", key="railway_dist")
                nearby_points.append(f"Railway Station ({distance})" if distance else "Railway Station")
        
        with col2:
            st.markdown("**Essential Services**")
            if st.checkbox("School", value=False, key="nearby_school"):
                nearby_points.append("School Nearby")
            
            if st.checkbox("Hospital", value=False, key="nearby_hospital"):
                nearby_points.append("Hospital Nearby")
            
            if st.checkbox("Market/Mall", value=False, key="nearby_market"):
                nearby_points.append("Shopping Complex")
            
            if st.checkbox("Restaurant/Cafe", value=False, key="nearby_restaurant"):
                nearby_points.append("Restaurants")
        
        st.divider()
        
        st.markdown("#### 📄 Additional Description (Optional)")
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.info("💡 **Tip:** Add unique selling points here - corner flat, sea view, renovated recently, premium fittings, etc. This will be incorporated into the AI-generated description!")
        rough_description = st.text_area(
            "Owner's Description / Special Features",
            placeholder="Add any additional details, special features, or unique selling points...\n\nExamples:\n- Corner flat with cross ventilation\n- Recently renovated with Italian marble\n- Sea-facing balcony with sunset views\n- Vastu compliant\n- Premium society with celebrity residents",
            height=150,
            help="Free text to add any extra information about the property. This will be prominently featured in the generated description.",
            key="rough_desc"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Prepare property data
    property_data = {
        'property_type': property_type.lower(),
        'bhk': bhk,
        'area_sqft': area_sqft,
        'area_unit': area_unit,
        'state': state,
        'district': district,
        'city': city,
        'locality': locality,
        'pincode': pincode if pincode else '',
        'landmark': landmark if landmark else '',
        'floor_no': floor_no,
        'total_floors': total_floors,
        'furnishing_status': furnishing.lower(),
        'rent_amount': rent,
        'deposit_amount': deposit,
        'maintenance': maintenance,
        'parking_charges': parking_charges,
        'negotiable': negotiable,
        'available_from': str(available),
        'preferred_tenants': ', '.join(preferred_tenants),
        'amenities': amenities,
        'water_supply': water_sources,
        'water_availability': water_availability,
        'nearby_points': nearby_points,
        'rough_description': rough_description if rough_description else ''
    }
    
    # Action buttons section
    st.markdown("---")
    st.markdown("### 🚀 Generate Description")
    
    # Show current variation style hint
    if st.session_state.generation_count > 0:
        variation_styles = [
            "🌟 Lifestyle & Experience",
            "💰 Investment & Value", 
            "📍 Location & Connectivity",
            "✨ Comfort & Luxury",
            "👨‍👩‍👧 Community & Safety"
        ]
        next_style = variation_styles[(st.session_state.generation_count) % 5]
        st.info(f"🔄 Next regeneration will use style: **{next_style}**")
    
    # Generate and Regenerate buttons with better layout
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([2, 1, 1, 1])
    
    with btn_col1:
        generate_clicked = st.button("🎯 Generate Premium Description", 
                                   type="primary", 
                                   use_container_width=True, 
                                   key="generate_btn")
    
    with btn_col2:
        regenerate_clicked = st.button("🔄 Regenerate", 
                                     type="secondary", 
                                     use_container_width=True, 
                                     disabled=st.session_state.generated_result is None,
                                     help="Generate a different version with same details",
                                     key="regenerate_btn")
    
    with btn_col3:
        clear_clicked = st.button("🗑️ Clear", 
                                type="secondary", 
                                use_container_width=True,
                                disabled=st.session_state.generated_result is None,
                                help="Clear generated results",
                                key="clear_btn")
    
    with btn_col4:
        if st.session_state.generated_result:
            st.markdown('<div class="success-badge">Generated</div>', unsafe_allow_html=True)
    
    # Handle clear
    if clear_clicked:
        st.session_state.generated_result = None
        st.session_state.generation_count = 0
        st.session_state.enhanced_description = None
        st.session_state.use_enhanced = False
        st.session_state.enhanced_edit_mode = False
        st.rerun()
    
    # Handle generation
    if generate_clicked or regenerate_clicked:
        if not city or not locality:
            st.error("❌ Please fill in all required fields marked with *")
            return
        
        st.session_state.property_data = property_data
        st.session_state.enhanced_description = None  # Reset enhanced on new generation
        st.session_state.use_enhanced = False
        st.session_state.enhanced_edit_mode = False
        
        if regenerate_clicked:
            st.session_state.generation_count += 1
            variation_styles = [
                "🌟 Lifestyle & Experience",
                "💰 Investment & Value", 
                "📍 Location & Connectivity",
                "✨ Comfort & Luxury",
                "👨‍👩‍👧 Community & Safety"
            ]
            current_style = variation_styles[st.session_state.generation_count % 5]
            st.info(f"🔄 Generating version #{st.session_state.generation_count + 1} with style: **{current_style}**")
        else:
            st.session_state.generation_count = 0
        
        # Progress bar for generation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"✨ Generating premium description... {i+1}%")
            time.sleep(0.01)
        
        result = generate_description(
            property_data, 
            api_provider, 
            api_key,
            variation_seed=st.session_state.generation_count
        )
        
        progress_bar.empty()
        status_text.empty()
        
        if result:
            st.session_state.generated_result = result
            st.balloons()
            st.success("✅ Premium Description Generated Successfully!")
    
    # Display results with enhanced UI
    if st.session_state.generated_result:
        result = st.session_state.generated_result
        property_data = st.session_state.property_data
        
        # Show version info with style
        variation_styles = [
            "🌟 Lifestyle & Experience",
            "💰 Investment & Value", 
            "📍 Location & Connectivity",
            "✨ Comfort & Luxury",
            "👨‍👩‍👧 Community & Safety"
        ]
        current_style = variation_styles[st.session_state.generation_count % 5]
        
        st.markdown("---")
        
        # Results header
        col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
        with col_header1:
            st.markdown(f"## 📝 Generated Description")
        with col_header2:
            st.markdown(f'<div class="info-badge">Version #{st.session_state.generation_count + 1}</div>', unsafe_allow_html=True)
        with col_header3:
            st.markdown(f'<div class="success-badge">{current_style}</div>', unsafe_allow_html=True)
        
        # Editable Title
        st.markdown("### 🏷️ Property Title")
        edited_title = st.text_input(
            "Title (Edit as needed)",
            value=result['title'],
            key="edit_title",
            help="Click to edit the generated title",
            label_visibility="collapsed"
        )
        
        # Editable Teaser
        edited_teaser = st.text_input(
            "Teaser Line (Edit as needed)",
            value=result['teaser_text'],
            key="edit_teaser",
            help="Click to edit the teaser text",
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Enhanced description section with tabs
        st.markdown("### 📝 Full Description")
        
        desc_tab1, desc_tab2, desc_tab3 = st.tabs(["✏️ Edit Description", "🚀 AI Enhanced Version", "📊 Compare Versions"])
        
        with desc_tab1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.info("💡 **Tip:** Edit the description below as needed. Your changes will be saved in downloads.")
            edited_description = st.text_area(
                "Description (Edit as needed)",
                value=result['full_description'],
                height=250,
                key="edit_description",
                help="Click to edit the generated description",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with desc_tab2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 🚀 AI Enhanced Version")
            st.caption("Generate an enhanced, more detailed version of the description")
            
            # Initialize enhanced description in session state
            if 'enhanced_description' not in st.session_state:
                st.session_state.enhanced_description = None
            
            col_enhance1, col_enhance2 = st.columns([1, 1])
            
            with col_enhance1:
                enhance_style = st.selectbox(
                    "Enhancement Style",
                    ["More Detailed & Elaborate", "More Emotional & Persuasive", "More Professional & Formal", 
                     "Add Local Flavor & Culture", "Focus on Investment Value", "Luxury & Premium Feel"],
                    key="enhance_style"
                )
            
            with col_enhance2:
                enhance_length = st.selectbox(
                    "Target Length",
                    ["Medium (200-250 words)", "Long (300-350 words)", "Extra Long (400-500 words)"],
                    key="enhance_length"
                )
            
            if st.button("✨ Generate Enhanced Version", type="primary", key="enhance_btn", use_container_width=True):
                if api_key:
                    with st.spinner("🚀 Enhancing description with AI..."):
                        enhanced = generate_enhanced_description(
                            original_desc=result['full_description'],
                            property_data=property_data,
                            style=enhance_style,
                            length=enhance_length,
                            api_key=api_key
                        )
                        if enhanced:
                            st.session_state.enhanced_description = enhanced
                            st.success("✅ Enhanced version generated!")
                else:
                    st.error("❌ Please enter Groq API key in sidebar to use AI enhancement")
            
            # Display enhanced version if available
            if st.session_state.enhanced_description:
                st.markdown("---")
                st.markdown("**Enhanced Description:**")
                
                # Initialize edit mode in session state
                if 'enhanced_edit_mode' not in st.session_state:
                    st.session_state.enhanced_edit_mode = False
                
                # Show either view mode or edit mode
                if st.session_state.enhanced_edit_mode:
                    # Edit Mode - Editable text area
                    st.info("✏️ **Edit Mode** - Make your changes below")
                    enhanced_edited = st.text_area(
                        "Edit Enhanced Version",
                        value=st.session_state.enhanced_description,
                        height=300,
                        key="enhanced_desc_edit"
                    )
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("💾 Save Changes", type="primary", key="save_enhanced_edit", use_container_width=True):
                            st.session_state.enhanced_description = enhanced_edited
                            st.session_state.enhanced_edit_mode = False
                            st.rerun()
                    with col_cancel:
                        if st.button("❌ Cancel", key="cancel_enhanced_edit", use_container_width=True):
                            st.session_state.enhanced_edit_mode = False
                            st.rerun()
                else:
                    # View Mode - Read only display with better styling
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 10px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
                    {st.session_state.enhanced_description}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    word_count = len(st.session_state.enhanced_description.split())
                    st.caption(f"📏 Word Count: {word_count}")
                    
                    # Action buttons
                    col_edit, col_use, col_regen = st.columns(3)
                    with col_edit:
                        if st.button("✏️ Edit", key="edit_enhanced_btn", use_container_width=True):
                            st.session_state.enhanced_edit_mode = True
                            st.rerun()
                    with col_use:
                        use_enhanced = st.checkbox(
                            "✅ Use in Downloads", 
                            value=st.session_state.get('use_enhanced', False),
                            key="use_enhanced_checkbox"
                        )
                        if use_enhanced:
                            st.session_state.use_enhanced = True
                        else:
                            st.session_state.use_enhanced = False
                    with col_regen:
                        if st.button("🔄 Regenerate", key="regenerate_enhanced", use_container_width=True):
                            st.session_state.enhanced_description = None
                            st.session_state.enhanced_edit_mode = False
                            st.rerun()
            else:
                st.info("👆 Click 'Generate Enhanced Version' to create an improved description")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with desc_tab3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Compare: Original vs Enhanced")
            
            compare_col1, compare_col2 = st.columns(2)
            
            with compare_col1:
                st.markdown("**🔵 Original AI Generated:**")
                st.text_area(
                    "Original",
                    value=result['full_description'],
                    height=250,
                    disabled=True,
                    key="compare_original",
                    label_visibility="collapsed"
                )
                word_count_orig = len(result['full_description'].split())
                st.caption(f"📏 Word Count: {word_count_orig}")
            
            with compare_col2:
                st.markdown("**🟢 Enhanced Version:**")
                if st.session_state.enhanced_description:
                    st.text_area(
                        "Enhanced",
                        value=st.session_state.enhanced_description,
                        height=250,
                        disabled=True,
                        key="compare_enhanced",
                        label_visibility="collapsed"
                    )
                    word_count_enh = len(st.session_state.enhanced_description.split())
                    st.caption(f"📏 Word Count: {word_count_enh} ({word_count_enh - word_count_orig:+d} words)")
                else:
                    st.info("Generate enhanced version first to compare")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Determine which description to use for downloads
        use_enhanced_version = st.session_state.get('use_enhanced', False)
        if use_enhanced_version and st.session_state.enhanced_description:
            final_description = st.session_state.enhanced_description
        else:
            final_description = edited_description
        
        st.divider()
        
        # Features and SEO section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### ✨ Key Features")
            st.info("💡 Edit each feature below:")
            edited_bullets = []
            for i, point in enumerate(result['bullet_points'], 1):
                edited_point = st.text_input(
                    f"Feature {i}",
                    value=point,
                    key=f"edit_bullet_{i}",
                    label_visibility="collapsed"
                )
                edited_bullets.append(edited_point)
                st.markdown(f"<div class='feature-card'><strong>{i}.</strong> {edited_point}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### 🔍 SEO Optimization")
            edited_keywords = st.text_input(
                "Keywords (comma separated)",
                value=", ".join(result['seo_keywords']),
                key="edit_keywords"
            )
            edited_keywords_list = [k.strip() for k in edited_keywords.split(",")]
            
            st.markdown("### 📊 SEO Metadata")
            edited_meta_title = st.text_input(
                "Meta Title",
                value=result['meta_title'],
                key="edit_meta_title"
            )
            edited_meta_desc = st.text_area(
                "Meta Description",
                value=result['meta_description'],
                height=100,
                key="edit_meta_desc"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Store edited values for download
        edited_result = {
            'title': edited_title,
            'teaser_text': edited_teaser,
            'full_description': final_description,  # Uses enhanced version if selected
            'bullet_points': edited_bullets,
            'seo_keywords': edited_keywords_list,
            'meta_title': edited_meta_title,
            'meta_description': edited_meta_desc
        }
        
        st.divider()
        
        # Download options with enhanced UI
        st.markdown("### 💾 Download Options")
        st.success("✅ Downloads will include your edited content!")
        
        download_col1, download_col2, download_col3 = st.columns(3)
        
        with download_col1:
            json_data = json.dumps({
                'property_details': property_data,
                'generated_content': edited_result,
                'original_content': result,
                'generation_version': st.session_state.generation_count + 1,
                'style_used': current_style
            }, indent=2)
            st.download_button(
                "📄 Download JSON",
                json_data,
                f"property_{property_data['locality'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_v{st.session_state.generation_count + 1}.json",
                "application/json",
                use_container_width=True,
                key="download_json"
            )
        
        with download_col2:
            text_content = f"""{edited_result['title']}
{edited_result['teaser_text']}

{edited_result['full_description']}

Key Features:
{chr(10).join(f"• {p}" for p in edited_result['bullet_points'])}

SEO Keywords: {', '.join(edited_result['seo_keywords'])}
Meta Title: {edited_result['meta_title']}
Meta Description: {edited_result['meta_description']}

---
Property: {property_data['bhk']} {property_data['property_type'].title()}
Location: {property_data['locality']}, {property_data['city']}
Rent: ₹{property_data['rent_amount']:,}/month

Version: #{st.session_state.generation_count + 1}
Style: {current_style}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            st.download_button(
                "📝 Download TXT",
                text_content,
                f"property_{property_data['locality'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_v{st.session_state.generation_count + 1}.txt",
                "text/plain",
                use_container_width=True,
                key="download_txt"
            )
        
        with download_col3:
            csv_data = pd.DataFrame([{
                'Property_Type': property_data['property_type'],
                'BHK': property_data['bhk'],
                'Area': f"{property_data['area_sqft']} {property_data['area_unit']}",
                'Location': f"{property_data['locality']}, {property_data['city']}, {property_data.get('district', '')}, {property_data.get('state', '')}",
                'Pincode': property_data.get('pincode', ''),
                'Rent': property_data['rent_amount'],
                'Title': edited_result['title'],
                'Teaser': edited_result['teaser_text'],
                'Description': edited_result['full_description'],
                'Features': ' | '.join(edited_result['bullet_points']),
                'SEO_Keywords': ', '.join(edited_result['seo_keywords']),
                'Meta_Title': edited_result['meta_title'],
                'Meta_Description': edited_result['meta_description'],
                'Version': st.session_state.generation_count + 1,
                'Style': current_style
            }])
            
            st.download_button(
                "📊 Download CSV",
                csv_data.to_csv(index=False),
                f"property_{property_data['locality'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_v{st.session_state.generation_count + 1}.csv",
                "text/csv",
                use_container_width=True,
                key="download_csv"
            )


if __name__ == "__main__":
    main()