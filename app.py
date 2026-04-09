import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة البيانات الشاملة (مع إضافة الفورو 11، 13، 16، 20)
DATABASE_PRO = {
    # الفورو (Tubes/Foureaux)
    "Foureau Orange 11mm (Rouleau)": 28.000,
    "Foureau Orange 13mm (Rouleau)": 32.000,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.000,
    "Foureau Noir (Béton) 16mm": 42.000,
    "Foureau Noir (Béton) 20mm": 52.000,
    
    # الحماية (Hager)
    "Hager: Disjoncteur DPN 10A": 10.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800,
    "Hager: Différentiel 40A 30mA": 95.000,
    "Hager: Coffret Encastré 12M": 48.000,
    "Hager: Coffret Encastré 24M": 145.000,

    # الأجهزة (Legrand Valena)
    "Legrand Valena: Interrupteur Simple": 8.800,
    "Legrand Valena: Va et Vient": 10.500,
    "Legrand Valena: Prise 2P+T": 11.200,

    # الأجهزة (Générale)
    "Générale Sys45: Interrupteur Simple": 5.500,
    "Générale Sys45: Va et Vient": 6.800,
    "Générale: Boite Encastrement 3M": 0.900,
    "Générale:
