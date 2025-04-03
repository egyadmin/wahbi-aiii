
"""
وحدة التسعير الموجه للربحية
"""
import streamlit as st
import pandas as pd

def calculate_profit_oriented_price(costs, target_profit=0.25):
    """حساب السعر الموجه للربحية"""
    base_cost = sum(costs.values())
    required_price = base_cost / (1 - target_profit)
    
    return {
        "base_cost": base_cost,
        "target_profit_margin": target_profit,
        "required_price": required_price,
        "expected_profit": required_price - base_cost
    }

def render_profit_driven_strategy():
    """عرض واجهة التسعير الموجه للربحية"""
    st.header("التسعير الموجه للربحية")
    
    target_profit = st.slider(
        "هامش الربح المستهدف",
        min_value=0.10,
        max_value=0.40,
        value=0.25,
        format="%d%%"
    )
    
    st.info("هذه الاستراتيجية تركز على تحقيق هامش ربح مستهدف مع الأخذ في الاعتبار تكاليف المشروع الأساسية")
    
    return target_profit
