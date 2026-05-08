#!/usr/bin/env python3
"""
Quadratic Equation Solver with Streamlit UI
Supports rational equations: ax² + bx + c = 0
"""

import streamlit as st
import math
from fractions import Fraction
from decimal import Decimal

# Page config
st.set_page_config(
    page_title="Quadratic Equation Solver",
    page_icon="📐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .solution-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .equation-display {
        font-size: 24px;
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📐 Quadratic Equation Solver")
st.markdown("### Solve equations of the form: *ax² + bx + c = 0*")

# Sidebar for input method
with st.sidebar:
    st.header("Input Method")
    input_type = st.radio(
        "Choose how to enter coefficients:",
        ["Simple (Decimal)", "Fraction (numerator/denominator)"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This solver handles:
    - Real and complex roots
    - Fractional coefficients
    - Shows discriminant analysis
    - Provides step-by-step solution
    """)

# Main input area
col1, col2, col3 = st.columns(3)

def parse_fraction_input(fraction_str):
    """Parse fraction input like '3/4' or '1/3'"""
    fraction_str = fraction_str.strip()
    if not fraction_str:
        return None
    
    try:
        if '/' in fraction_str:
            parts = fraction_str.split('/')
            if len(parts) == 2:
                num = float(parts[0])
                den = float(parts[1])
                if den == 0:
                    return None
                return num / den
            else:
                return None
        else:
            return float(fraction_str)
    except:
        return None

def parse_coefficient(value_str, is_fraction_mode):
    """Parse coefficient from string input"""
    if is_fraction_mode:
        result = parse_fraction_input(value_str)
        if result is not None:
            return Fraction(value_str).limit_denominator()
        return None
    else:
        try:
            return float(value_str)
        except:
            return None

# Input fields
with col1:
    st.markdown("#### Coefficient **a**")
    if input_type == "Simple (Decimal)":
        a_str = st.text_input("Enter a:", value="1", key="a", help="Coefficient of x²")
        a = parse_coefficient(a_str, False)
    else:
        a_str = st.text_input("Enter a:", value="1", key="a_frac", help="Use fractions like 3/4")
        a = parse_coefficient(a_str, True)

with col2:
    st.markdown("#### Coefficient **b**")
    if input_type == "Simple (Decimal)":
        b_str = st.text_input("Enter b:", value="-3", key="b", help="Coefficient of x")
        b = parse_coefficient(b_str, False)
    else:
        b_str = st.text_input("Enter b:", value="-5/2", key="b_frac", help="Use fractions like -5/2")
        b = parse_coefficient(b_str, True)

with col3:
    st.markdown("#### Coefficient **c**")
    if input_type == "Simple (Decimal)":
        c_str = st.text_input("Enter c:", value="2", key="c", help="Constant term")
        c = parse_coefficient(c_str, False)
    else:
        c_str = st.text_input("Enter c:", value="3/4", key="c_frac", help="Use fractions like 3/4")
        c = parse_coefficient(c_str, True)

# Display the equation
if a is not None and b is not None and c is not None:
    # Format equation display
    a_display = str(Fraction(a).limit_denominator()) if isinstance(a, Fraction) else f"{a:g}"
    b_display = str(Fraction(b).limit_denominator()) if isinstance(b, Fraction) else f"{b:g}"
    c_display = str(Fraction(c).limit_denominator()) if isinstance(c, Fraction) else f"{c:g}"
    
    if b >= 0:
        eq_str = f"{a_display}x² + {abs(b):g}x + {c_display} = 0"
    else:
        eq_str = f"{a_display}x² - {abs(b):g}x + {c_display} = 0" if c >= 0 else f"{a_display}x² - {abs(b):g}x - {abs(c):g} = 0"
    
    st.markdown(f'<div class="equation-display">{eq_str}</div>', unsafe_allow_html=True)
    
    # Solve button
    if st.button("🔍 Solve Equation", type="primary", use_container_width=True):
        # Convert to float for calculations
        a_float = float(a)
        b_float = float(b)
        c_float = float(c)
        
        # Check if it's a quadratic equation
        if a_float == 0:
            st.error("Error: 'a' cannot be zero for a quadratic equation.")
            if b_float != 0:
                x = -c_float / b_float
                st.info(f"This is actually a linear equation. Solution: x = {x:.4f}")
        else:
            # Calculate discriminant
            discriminant = b_float**2 - 4*a_float*c_float
            
            # Create columns for results
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown("### 📊 Analysis")
                st.markdown(f"""
                **Discriminant (Δ):** {discriminant:.6f}
                
                **Nature of roots:**
                """)
                
                if discriminant > 0:
                    st.success("✅ Two distinct real roots")
                elif discriminant == 0:
                    st.warning("⚡ One real root (repeated)")
                else:
                    st.info("🔮 Two complex conjugate roots")
            
            with res_col2:
                st.markdown("### 🎯 Solutions")
                
                if discriminant > 0:
                    # Two real roots
                    sqrt_disc = math.sqrt(discriminant)
                    x1 = (-b_float + sqrt_disc) / (2*a_float)
                    x2 = (-b_float - sqrt_disc) / (2*a_float)
                    
                    st.markdown(f"""
                    <div class="solution-box">
                    <h4>x₁ = {x1:.6f}</h4>
                    <h4>x₂ = {x2:.6f}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show fractional approximations
                    try:
                        x1_frac = Fraction(x1).limit_denominator(1000)
                        x2_frac = Fraction(x2).limit_denominator(1000)
                        if x1_frac.denominator <= 1000 or x2_frac.denominator <= 1000:
                            st.caption(f"Fractional approximations: x₁ ≈ {x1_frac}, x₂ ≈ {x2_frac}")
                    except:
                        pass
                    
                elif discriminant == 0:
                    # One repeated root
                    x = -b_float / (2*a_float)
                    st.markdown(f"""
                    <div class="solution-box">
                    <h4>x = {x:.6f} (repeated root)</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        x_frac = Fraction(x).limit_denominator(1000)
                        st.caption(f"Fractional approximation: x ≈ {x_frac}")
                    except:
                        pass
                    
                else:
                    # Complex roots
                    real_part = -b_float / (2*a_float)
                    imag_part = math.sqrt(abs(discriminant)) / (2*a_float)
                    
                    st.markdown(f"""
                    <div class="solution-box">
                    <h4>x₁ = {real_part:.6f} + {imag_part:.6f}i</h4>
                    <h4>x₂ = {real_part:.6f} - {imag_part:.6f}i</h4>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Step-by-step solution
            with st.expander("📝 Show step-by-step solution"):
                st.markdown(f"""
                #### Step 1: Identify coefficients
                - a = {a_float}
                - b = {b_float}
                - c = {c_float}
                
                #### Step 2: Calculate discriminant
                Δ = b² - 4ac
                Δ = ({b_float})² - 4({a_float})({c_float})
                Δ = {b_float**2} - {4*a_float*c_float}
                Δ = {discriminant}
                
                #### Step 3: Apply quadratic formula
                x = (-b ± √Δ) / (2a)
                """)
                
                if discriminant >= 0:
                    st.markdown(f"""
                    x = (-({b_float}) ± √{discriminant}) / (2({a_float}))
                    x = ({-b_float} ± {math.sqrt(discriminant):.4f}) / {2*a_float}
                    """)
                else:
                    st.markdown(f"""
                    Since Δ < 0, we have complex roots:
                    x = (-({b_float}) ± √({discriminant})) / (2({a_float}))
                    x = ({-b_float} ± {math.sqrt(abs(discriminant)):.4f}i) / {2*a_float}
                    """)
                
                st.markdown("#### Step 4: Final solutions")
                if discriminant > 0:
                    x1 = (-b_float + math.sqrt(discriminant)) / (2*a_float)
                    x2 = (-b_float - math.sqrt(discriminant)) / (2*a_float)
                    st.markdown(f"""
                    - x₁ = {x1:.6f}
                    - x₂ = {x2:.6f}
                    """)
                elif discriminant == 0:
                    x = -b_float / (2*a_float)
                    st.markdown(f"- x = {x:.6f} (repeated)")
                else:
                    real_part = -b_float / (2*a_float)
                    imag_part = math.sqrt(abs(discriminant)) / (2*a_float)
                    st.markdown(f"""
                    - x₁ = {real_part:.6f} + {imag_part:.6f}i
                    - x₂ = {real_part:.6f} - {imag_part:.6f}i
                    """)
            
            # Verification
            with st.expander("✅ Verify solutions"):
                st.markdown("#### Plug solutions back into the equation:")
                if discriminant > 0:
                    x1 = (-b_float + math.sqrt(discriminant)) / (2*a_float)
                    x2 = (-b_float - math.sqrt(discriminant)) / (2*a_float)
                    result1 = a_float*x1**2 + b_float*x1 + c_float
                    result2 = a_float*x2**2 + b_float*x2 + c_float
                    st.markdown(f"""
                    For x₁ = {x1:.6f}:  
                    {a_float}({x1:.6f})² + {b_float}({x1:.6f}) + {c_float} = {result1:.10f}
                    
                    For x₂ = {x2:.6f}:  
                    {a_float}({x2:.6f})² + {b_float}({x2:.6f}) + {c_float} = {result2:.10f}
                    """)
                elif discriminant == 0:
                    x = -b_float / (2*a_float)
                    result = a_float*x**2 + b_float*x + c_float
                    st.markdown(f"""
                    For x = {x:.6f}:  
                    {a_float}({x:.6f})² + {b_float}({x:.6f}) + {c_float} = {result:.10f}
                    """)

else:
    st.info("Please enter valid coefficients for a, b, and c to solve the quadratic equation.")

# Footer
st.markdown("---")
st.caption("💡 Tip: You can use fractions like '1/3' or decimals like '0.333' for coefficients")
