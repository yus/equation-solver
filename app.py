#!/usr/bin/env python3
"""
Quadratic Equation Solver v2.0.1
Solves equations of form: ax² + bx + c = 0 with graphical visualization
"""

import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from fractions import Fraction

# Version
VERSION = "2.0.1"

# Page config
st.set_page_config(
    page_title="Equation Solver",
    page_icon="📐",
    layout="wide"
)

# Minimal custom CSS
st.markdown("""
<style>
    .equation-display {
        font-size: 24px;
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 20px 0;
    }
    .solution-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Quadratic Equation Solver")
st.markdown("##### *ax² + bx + c = 0*")

# Sidebar
with st.sidebar:
    st.header("Input")
    input_type = st.radio(
        "Format:",
        ["Decimal", "Fraction (a/b)"]
    )
    
    st.markdown("---")
    st.caption(f"v{VERSION}")

def parse_fraction_input(fraction_str):
    """Parse fraction input like '3/4'"""
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

def create_quadratic_plot(a, b, c, roots=None):
    """Create interactive plot of quadratic function with roots"""
    # Generate x values
    if roots and len(roots) > 0:
        # Center around roots with some padding
        if isinstance(roots[0], complex):
            center = -b / (2*a)
        else:
            center = sum(roots) / len(roots)
        x_min = center - 5
        x_max = center + 5
    else:
        x_min, x_max = -5, 5
    
    x = np.linspace(x_min, x_max, 200)
    y = a * x**2 + b * x + c
    
    # Create figure
    fig = go.Figure()
    
    # Add quadratic curve
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        mode='lines',
        name=f'{a}x² + {b}x + {c}',
        line=dict(color='#667eea', width=2)
    ))
    
    # Add x-axis
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add roots if they exist and are real
    if roots:
        real_roots = [r for r in roots if not isinstance(r, complex)]
        if real_roots:
            root_y = [0] * len(real_roots)
            fig.add_trace(go.Scatter(
                x=real_roots,
                y=root_y,
                mode='markers',
                name='Roots',
                marker=dict(color='red', size=10, symbol='x'),
                hovertemplate='x = %{x:.4f}<br>y = 0<extra></extra>'
            ))
    
    # Add vertex
    vertex_x = -b / (2*a)
    vertex_y = a * vertex_x**2 + b * vertex_x + c
    fig.add_trace(go.Scatter(
        x=[vertex_x],
        y=[vertex_y],
        mode='markers',
        name='Vertex',
        marker=dict(color='green', size=8, symbol='diamond'),
        hovertemplate='Vertex: (%{x:.4f}, %{y:.4f})<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Graph of f(x) = {a}x² + {b}x + {c}",
        xaxis_title="x",
        yaxis_title="f(x)",
        showlegend=True,
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    return fig

# Main input area
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**a** (x²)")
    if input_type == "Decimal":
        a_str = st.text_input("a", value="1", key="a", label_visibility="collapsed")
        a = parse_coefficient(a_str, False)
    else:
        a_str = st.text_input("a (fraction)", value="1", key="a_frac", label_visibility="collapsed")
        a = parse_coefficient(a_str, True)

with col2:
    st.markdown("**b** (x)")
    if input_type == "Decimal":
        b_str = st.text_input("b", value="-3", key="b", label_visibility="collapsed")
        b = parse_coefficient(b_str, False)
    else:
        b_str = st.text_input("b (fraction)", value="-5/2", key="b_frac", label_visibility="collapsed")
        b = parse_coefficient(b_str, True)

with col3:
    st.markdown("**c**")
    if input_type == "Decimal":
        c_str = st.text_input("c", value="2", key="c", label_visibility="collapsed")
        c = parse_coefficient(c_str, False)
    else:
        c_str = st.text_input("c (fraction)", value="3/4", key="c_frac", label_visibility="collapsed")
        c = parse_coefficient(c_str, True)

# Display equation and solve
if a is not None and b is not None and c is not None:
    # Format for display
    a_display = str(Fraction(a).limit_denominator()) if isinstance(a, Fraction) else f"{a:g}"
    b_display = str(Fraction(b).limit_denominator()) if isinstance(b, Fraction) else f"{b:g}"
    c_display = str(Fraction(c).limit_denominator()) if isinstance(c, Fraction) else f"{c:g}"
    
    st.markdown(f'<div class="equation-display">{a_display}x² + {b_display}x + {c_display} = 0</div>', unsafe_allow_html=True)
    
    if st.button("Solve", type="primary", use_container_width=True):
        a_float = float(a)
        b_float = float(b)
        c_float = float(c)
        
        if a_float == 0:
            st.error("Not a quadratic equation (a = 0)")
            if b_float != 0:
                x = -c_float / b_float
                st.info(f"Linear solution: x = {x:.4f}")
        else:
            # Calculate discriminant and roots
            discriminant = b_float**2 - 4*a_float*c_float
            
            # Prepare roots list for plotting
            roots = []
            
            if discriminant > 0:
                sqrt_disc = math.sqrt(discriminant)
                x1 = (-b_float + sqrt_disc) / (2*a_float)
                x2 = (-b_float - sqrt_disc) / (2*a_float)
                roots = [x1, x2]
            elif discriminant == 0:
                x = -b_float / (2*a_float)
                roots = [x]
            else:
                real_part = -b_float / (2*a_float)
                imag_part = math.sqrt(abs(discriminant)) / (2*a_float)
                roots = [complex(real_part, imag_part), complex(real_part, -imag_part)]
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["Solutions", "Graph", "Step-by-step"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Analysis")
                    st.markdown(f"**Δ = {discriminant:.4f}**")
                    
                    if discriminant > 0:
                        st.success("Two real roots")
                    elif discriminant == 0:
                        st.warning("One real root (double)")
                    else:
                        st.info("Complex conjugate roots")
                
                with col2:
                    st.markdown("### Roots")
                    
                    if discriminant > 0:
                        st.markdown(f"""
                        <div class="solution-box">
                        x₁ = {roots[0]:.4f}<br>
                        x₂ = {roots[1]:.4f}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Try fractional representation
                        try:
                            x1_frac = Fraction(roots[0]).limit_denominator(1000)
                            x2_frac = Fraction(roots[1]).limit_denominator(1000)
                            st.caption(f"≈ {x1_frac}, {x2_frac}")
                        except:
                            pass
                            
                    elif discriminant == 0:
                        st.markdown(f"""
                        <div class="solution-box">
                        x = {roots[0]:.4f} (double)
                        </div>
                        """, unsafe_allow_html=True)
                        
                        try:
                            x_frac = Fraction(roots[0]).limit_denominator(1000)
                            st.caption(f"≈ {x_frac}")
                        except:
                            pass
                    else:
                        st.markdown(f"""
                        <div class="solution-box">
                        x₁ = {roots[0].real:.4f} + {roots[0].imag:.4f}i<br>
                        x₂ = {roots[1].real:.4f} - {roots[1].imag:.4f}i
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("### Graph")
                fig = create_quadratic_plot(a_float, b_float, c_float, roots)
                st.plotly_chart(fig, use_container_width=True)
                
                # Vertex info
                vertex_x = -b_float / (2*a_float)
                vertex_y = a_float * vertex_x**2 + b_float * vertex_x + c_float
                st.caption(f"Vertex: ({vertex_x:.4f}, {vertex_y:.4f})")
            
            with tab3:
                st.markdown("### Step-by-step solution")
                st.markdown(f"""
                **Step 1: Identify coefficients**
                - a = {a_float}
                - b = {b_float}
                - c = {c_float}
                
                **Step 2: Calculate discriminant**
                Δ = b² - 4ac
                Δ = ({b_float})² - 4({a_float})({c_float})
                Δ = {b_float**2} - {4*a_float*c_float}
                Δ = {discriminant}
                
                **Step 3: Apply quadratic formula**
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
                
                st.markdown("**Step 4: Final solutions**")
                if discriminant > 0:
                    st.markdown(f"""
                    - x₁ = {roots[0]:.6f}
                    - x₂ = {roots[1]:.6f}
                    """)
                elif discriminant == 0:
                    st.markdown(f"- x = {roots[0]:.6f} (repeated)")
                else:
                    st.markdown(f"""
                    - x₁ = {roots[0].real:.6f} + {roots[0].imag:.6f}i
                    - x₂ = {roots[1].real:.6f} - {roots[1].imag:.6f}i
                    """)

else:
    st.info("Enter coefficients to solve")

# Footer
st.caption("—")
