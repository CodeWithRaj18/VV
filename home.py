import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import math

# --- STATIC STATION DATA (Total 220+ stations, original core) ---
HYDERABAD_STATIONS = [
    {"name": "E-Charge Gachibowli", "lat": 17.4475, "lon": 78.3750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "EV Point Hitech City", "lat": 17.4402, "lon": 78.3845, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Ather Grid Kondapur", "lat": 17.4580, "lon": 78.3761, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "ChargeZone Jubilee", "lat": 17.4320, "lon": 78.4010, "operator": "ChargeZone", "capacity": "120kW DC"},
    {"name": "Electric Park Banjara", "lat": 17.4125, "lon": 78.4350, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Smart Charge Begumpet", "lat": 17.4360, "lon": 78.4590, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Power Grid Sec-bad", "lat": 17.4480, "lon": 78.4900, "operator": "Ather", "capacity": "25kW AC"},
    {"name": "Fast Charger Tarnaka", "lat": 17.4385, "lon": 78.5320, "operator": "Tata Power", "capacity": "100kW DC"},
    {"name": "GreenVolt Uppal", "lat": 17.4010, "lon": 78.5550, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Mega Plug Kukatpally", "lat": 17.4930, "lon": 78.4050, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Volt Max Miyapur", "lat": 17.4980, "lon": 78.3610, "operator": "Go-E", "capacity": "25kW AC"},
    {"name": "NexiCharge Madhapur", "lat": 17.4485, "lon": 78.3915, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "EV Spot Manikonda", "lat": 17.4120, "lon": 78.3900, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Rapid Charge Ameerpet", "lat": 17.4390, "lon": 78.4480, "operator": "ChargeZone", "capacity": "15kW AC"},
    {"name": "City Volt Narayanaguda", "lat": 17.4050, "lon": 78.4850, "operator": "Relay Charge", "capacity": "50kW DC"},
    {"name": "Go Fast Mehdipatnam", "lat": 17.3980, "lon": 78.4410, "operator": "Go-E", "capacity": "25kW AC"},
    {"name": "Power Up Malakpet", "lat": 17.3750, "lon": 78.4920, "operator": "Ather", "capacity": "100kW DC"},
    {"name": "Future Charge Shamirpet", "lat": 17.6580, "lon": 78.5830, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Green Fuel Balanagar", "lat": 17.4680, "lon": 78.4710, "operator": "Tata Power", "capacity": "15kW AC"},
    {"name": "E-Drive Tolichowki", "lat": 17.4080, "lon": 78.4080, "operator": "Relay Charge", "capacity": "25kW AC"},
    {"name": "Charge Hub ECIL", "lat": 17.4650, "lon": 78.5800, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Ather Point DLF", "lat": 17.4400, "lon": 78.3755, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Go-E Station Mindspace", "lat": 17.4350, "lon": 78.3880, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Tata Quick Raidurgam", "lat": 17.4200, "lon": 78.3990, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "CZone Road No. 1", "lat": 17.4290, "lon": 78.4550, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "R-Charge Somajiguda", "lat": 17.4190, "lon": 78.4650, "operator": "Relay Charge", "capacity": "50kW DC"},
    {"name": "PowerHouse Punjagutta", "lat": 17.4300, "lon": 78.4500, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Ather Sec-bad West", "lat": 17.4420, "lon": 78.4780, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Green Energy Nacharam", "lat": 17.4500, "lon": 78.5600, "operator": "Tata Power", "capacity": "100kW DC"},
    {"name": "CZone LB Nagar", "lat": 17.3500, "lon": 78.5450, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "R-Charge Vanasthalipuram", "lat": 17.3300, "lon": 78.5500, "operator": "Relay Charge", "capacity": "25kW AC"},
    {"name": "Volt Max Shamshabad", "lat": 17.2500, "lon": 78.4300, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "NexiCharge Medipally", "lat": 17.4350, "lon": 78.5750, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "EV Spot Trimulgherry", "lat": 17.4690, "lon": 78.5150, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Rapid Charge Kompally", "lat": 17.5450, "lon": 78.4900, "operator": "ChargeZone", "capacity": "120kW DC"},
    {"name": "City Volt Chanda Nagar", "lat": 17.4850, "lon": 78.3050, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Go Fast Hafeezpet", "lat": 17.4780, "lon": 78.3350, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Power Up Lingampally", "lat": 17.4650, "lon": 78.2900, "operator": "Ather", "capacity": "25kW AC"},
]

# --- New Stations for Kandlakoya/Medchal area (Old additions) ---
KANDLAKOYA_MEDCHAL_STATIONS = [
    {"name": "Kandlakoya Hub", "lat": 17.6000, "lon": 78.4700, "operator": "Go-E", "capacity": "100kW DC"},
    {"name": "Medchal Service Point", "lat": 17.6300, "lon": 78.4800, "operator": "Tata Power", "capacity": "50kW AC"},
    {"name": "Girmapur EV Zone", "lat": 17.6150, "lon": 78.4550, "operator": "Ather", "capacity": "25kW AC"},
    {"name": "Kompally North Fast", "lat": 17.5600, "lon": 78.4850, "operator": "ChargeZone", "capacity": "120kW DC"},
    {"name": "Gundlapochampally Charge", "lat": 17.5500, "lon": 78.4500, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Gateway Medchal", "lat": 17.6400, "lon": 78.4600, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Outer Ring Charger N", "lat": 17.5900, "lon": 78.4400, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "EV Spot Shameerpet", "lat": 17.6200, "lon": 78.5000, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Medchal Railway Station", "lat": 17.6350, "lon": 78.4950, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Kandlakoya Industrial", "lat": 17.5950, "lon": 78.4650, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Medchal Bypass North", "lat": 17.6050, "lon": 78.4950, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Kandlakoya JNTU Rd", "lat": 17.6100, "lon": 78.4800, "operator": "Tata Power", "capacity": "25kW AC"},
   
    {"name": "Yadadri Service Point", "lat": 17.6180, "lon": 78.4750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Alwal Road North", "lat": 17.5880, "lon": 78.4680, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Mamidipally EV Stop", "lat": 17.5750, "lon": 78.4790, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Kompally Bypass East", "lat": 17.5650, "lon": 78.4950, "operator":  "ChargeZone", "capacity": "100kW DC"},
    {"name": "Medchal Rural Hub", "lat": 17.6450, "lon": 78.4650, "operator": "Relay Charge", "capacity": "15kW AC"},
]

# --- MASSIVE EXPANSION FOR FULL COVERAGE (Old City/East/Central coverage added) ---
FULL_HYDERABAD_COVERAGE = [
    {"name": "Old City Charminar", "lat": 17.3600, "lon": 78.4740, "operator": "Tata Power", "capacity": "100kW DC"},
    {"name": "Falaknuma Palace", "lat": 17.3315, "lon": 78.4450, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Afzal Gunj Market", "lat": 17.3870, "lon": 78.4670, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Khairatabad Circle", "lat": 17.4170, "lon": 78.4620, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Nampally Station West", "lat": 17.4080, "lon": 78.4640, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Basheerbagh Central", "lat": 17.4085, "lon": 78.4770, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Secunderabad Station East", "lat": 17.4390, "lon": 78.5030, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Malakpet Area 2", "lat": 17.3705, "lon": 78.4950, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Dilsukhnagar Metro", "lat": 17.3610, "lon": 78.5200, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Kothapet Central", "lat": 17.3680, "lon": 78.5350, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Uppal Ring Road", "lat": 17.3980, "lon": 78.5650, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Habsiguda East Side", "lat": 17.4395, "lon": 78.5450, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Nacharam Industrial", "lat": 17.4580, "lon": 78.5680, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "BHEL Township Gate", "lat": 17.5080, "lon": 78.3250, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Lingampally Central", "lat": 17.4670, "lon": 78.2880, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Chandanagar Market", "lat": 17.4780, "lon": 78.3080, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Miyapur Metro North", "lat": 17.5020, "lon": 78.3600, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kukatpally North", "lat": 17.5000, "lon": 78.3980, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Jeedimetla Industrial Hub", "lat": 17.5100, "lon": 78.4550, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Balanagar South", "lat": 17.4650, "lon": 78.4680, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Bowenpally West", "lat": 17.4550, "lon": 78.4750, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Trimulgherry Military", "lat": 17.4720, "lon": 78.5100, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Alwal Station South", "lat": 17.4800, "lon": 78.5000, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "ECIL X Roads 2", "lat": 17.4680, "lon": 78.5830, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Medipally East", "lat": 17.4320, "lon": 78.5780, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Vanasthalipuram East", "lat": 17.3280, "lon": 78.5530, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "LB Nagar South", "lat": 17.3480, "lon": 78.5400, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Attapur North", "lat": 17.3750, "lon": 78.4080, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Narsingi Highway", "lat": 17.3980, "lon": 78.3730, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Manikonda Main", "lat": 17.4100, "lon": 78.3920, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Mindspace North Gate", "lat": 17.4380, "lon": 78.3850, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Gachibowli Outer Ring N", "lat": 17.4500, "lon": 78.3320, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Miyapur Central", "lat": 17.4950, "lon": 78.3650, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Kukatpally Industrial", "lat": 17.4910, "lon": 78.4020, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Moosapet Metro", "lat": 17.4620, "lon": 78.4010, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Ameerpet Metro East", "lat": 17.4410, "lon": 78.4500, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Begumpet Airport", "lat": 17.4450, "lon": 78.4620, "operator": "Tata Power", "capacity": "120kW DC"},
    
    {"name": "Khairatabad West", "lat": 17.4190, "lon": 78.4580, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Lakdikapul Bridge", "lat": 17.4060, "lon": 78.4680, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Narayanguda Main", "lat": 17.4080, "lon": 78.4820, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Kachiguda Railway South", "lat": 17.3990, "lon": 78.4870, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Malakpet Metro", "lat": 17.3730, "lon": 78.4900, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Moosarambagh Central", "lat": 17.3720, "lon": 78.5080, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Musheerabad North", "lat": 17.4200, "lon": 78.5080, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Vidyanagar West", "lat": 17.4180, "lon": 78.5050, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Tarnaka East", "lat": 17.4400, "lon": 78.5350, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Nacharam Cross", "lat": 17.4520, "lon": 78.5580, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Uppal Stadium", "lat": 17.3950, "lon": 78.5600, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "ECIL Corner", "lat": 17.4670, "lon": 78.5850, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Sainikpuri North", "lat": 17.4900, "lon": 78.5650, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Kushaiguda Industrial", "lat": 17.5000, "lon": 78.5900, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Balanagar Industrial", "lat": 17.4700, "lon": 78.4700, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Moosapet Flyover", "lat": 17.4610, "lon": 78.3950, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Sanath Nagar", "lat": 17.4560, "lon": 78.4350, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Erragadda Metro", "lat": 17.4520, "lon": 78.4280, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Jubilee Hills Checkpost E", "lat": 17.4330, "lon": 78.4050, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kondapur Whitefields", "lat": 17.4585, "lon": 78.3800, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Hitech City Central", "lat": 17.4400, "lon": 78.3880, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Raidurgam West", "lat": 17.4180, "lon": 78.3970, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Khajaguda Hills", "lat": 17.4100, "lon": 78.3800, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Manikonda West", "lat": 17.4080, "lon": 78.3850, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Attapur North Bridge", "lat": 17.3780, "lon": 78.4120, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Mehdipatnam Military", "lat": 17.3950, "lon": 78.4350, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Rajendranagar East", "lat": 17.3500, "lon": 78.4100, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Gachibowli Financial", "lat": 17.4450, "lon": 78.3800, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Botanical Garden West", "lat": 17.4550, "lon": 78.3550, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "HITEX Exhibition", "lat": 17.4500, "lon": 78.3850, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Inorbit Mall Center", "lat": 17.4280, "lon": 78.3850, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Shilparamam Crafts", "lat": 17.4380, "lon": 78.3900, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Begumpet Central East", "lat": 17.4380, "lon": 78.4620, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Panjagutta Main Rd", "lat": 17.4290, "lon": 78.4550, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Nagarjuna Circle", "lat": 17.4250, "lon": 78.4580, "operator": "ChargeZone", "capacity": "25kW AC"},
    
    {"name": "Tank Bund South", "lat": 17.4100, "lon": 78.4820, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "RTC X Roads South", "lat": 17.4050, "lon": 78.4980, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Vidyanagar North", "lat": 17.4250, "lon": 78.5120, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Amberpet Main", "lat": 17.3970, "lon": 78.5100, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Dilsukhnagar Metro East", "lat": 17.3600, "lon": 78.5250, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Sultan Bazar", "lat": 17.3930, "lon": 78.4850, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Abids Market Center", "lat": 17.3900, "lon": 78.4780, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Moazam Jahi Market", "lat": 17.3900, "lon": 78.4680, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Masab Tank Area", "lat": 17.4030, "lon": 78.4480, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Toli Chowki West", "lat": 17.4050, "lon": 78.4050, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Qutb Shahi Tombs", "lat": 17.4180, "lon": 78.3900, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "IKEA Metro Station", "lat": 17.4300, "lon": 78.3750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Jeedimetla Road N", "lat": 17.5150, "lon": 78.4650, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kushaiguda Main", "lat": 17.4750, "lon": 78.5800, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "NFC Gate", "lat": 17.4600, "lon": 78.5650, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Osmania University Gate", "lat": 17.4180, "lon": 78.5300, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Mettuguda Rail Colony", "lat": 17.4400, "lon": 78.5100, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Chikkadpally Library", "lat": 17.4120, "lon": 78.4800, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Himayat Nagar Main", "lat": 17.4100, "lon": 78.4750, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Mallepally", "lat": 17.3980, "lon": 78.4550, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Dwaraka Circle", "lat": 17.4420, "lon": 78.3800, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Hussain Sagar North", "lat": 17.4250, "lon": 78.4880, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Cyber Towers North", "lat": 17.4550, "lon": 78.3800, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kondapur North", "lat": 17.4600, "lon": 78.3700, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Madhapur West", "lat": 17.4400, "lon": 78.3680, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Kukatpally Industrial 2", "lat": 17.4850, "lon": 78.4100, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Kandlakoya Hub", "lat": 17.6000, "lon": 78.4700, "operator": "Go-E", "capacity": "100kW DC"},
    {"name": "Medchal Service Point", "lat": 17.6300, "lon": 78.4800, "operator": "Tata Power", "capacity": "50kW AC"},
    {"name": "Girmapur EV Zone", "lat": 17.6150, "lon": 78.4550, "operator": "Ather", "capacity": "25kW AC"},
    {"name": "Kompally North Fast", "lat": 17.5600, "lon": 78.4850, "operator": "ChargeZone", "capacity": "120kW DC"},
    {"name": "Gundlapochampally Charge", "lat": 17.5500, "lon": 78.4500, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Gateway Medchal", "lat": 17.6400, "lon": 78.4600, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Outer Ring Charger N", "lat": 17.5900, "lon": 78.4400, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "EV Spot Shameerpet", "lat": 17.6200, "lon": 78.5000, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Medchal Railway Station", "lat": 17.6350, "lon": 78.4950, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Kandlakoya Industrial", "lat": 17.5950, "lon": 78.4650, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Medchal Bypass North", "lat": 17.6050, "lon": 78.4950, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Kandlakoya JNTU Rd", "lat": 17.6100, "lon": 78.4800, "operator": "Tata Power", "capacity": "25kW AC"},
   




    {"name": "Yadadri Service Point", "lat": 17.6180, "lon": 78.4750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Alwal Road North", "lat": 17.5880, "lon": 78.4680, "operator": "Tata Power", "capacity": "25kW AC"},
    {"name": "Mamidipally EV Stop", "lat": 17.5750, "lon": 78.4790, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Kompally Bypass East", "lat": 17.5650, "lon": 78.4950, "operator": "ChargeZone", "capacity": "100kW DC"},
    {"name": "Medchal Rural Hub", "lat": 17.6450, "lon": 78.4650, "operator": "Relay Charge", "capacity": "15kW AC"},
    # --- NEW 35 STATIONS ADDED FOR NORTH HYDERABAD DENSITY ---
    {"name": "Medchal North RTO", "lat": 17.6480, "lon": 78.4750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "ORR Medchal Entry", "lat": 17.6250, "lon": 78.4500, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kandlakoya Food Court", "lat": 17.6010, "lon": 78.4750, "operator": "Ather", "capacity": "25kW AC"},
    {"name": "Gundlapochampally South", "lat": 17.5450, "lon": 78.4400, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Dulapally Cross Road", "lat": 17.5700, "lon": 78.4350, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Kompally West Point", "lat": 17.5550, "lon": 78.4600, "operator": "Go-E", "capacity": "25kW AC"},
    {"name": "Jeedimetla Industrial Hub 2", "lat": 17.5120, "lon": 78.4450, "operator": "Tata Power", "capacity": "100kW DC"},
    {"name": "Balanagar X Roads North", "lat": 17.4750, "lon": 78.4800, "operator": "ChargeZone", "capacity": "50kW DC"},
    {"name": "Alwal Check Post", "lat": 17.5100, "lon": 78.5000, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Shamirpet Deer Park", "lat": 17.6100, "lon": 78.5250, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Medchal Town Center", "lat": 17.6380, "lon": 78.4850, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "ORR Exit 6 Service", "lat": 17.5950, "lon": 78.4480, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Pragathi Nagar (Quthbullapur)", "lat": 17.5050, "lon": 78.4150, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Suchitra Circle Fast", "lat": 17.4980, "lon": 78.4600, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "ECIL North Gate", "lat": 17.4720, "lon": 78.5750, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Aleru Road Hub", "lat": 17.6550, "lon": 78.4900, "operator": "Go-E", "capacity": "15kW AC"},
    {"name": "Kandlakoya Tech Park", "lat": 17.6080, "lon": 78.4650, "operator": "Tata Power", "capacity": "50kW DC"},
    {"name": "Medchal North Highway", "lat": 17.6200, "lon": 78.4700, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Gundlapochampally ORR", "lat": 17.5350, "lon": 78.4450, "operator": "Ather", "capacity": "6kW AC"},
    {"name": "Dulapally Village", "lat": 17.5750, "lon": 78.4250, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Kompally Main Cross", "lat": 17.5680, "lon": 78.4700, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Jeedimetla Road South", "lat": 17.4950, "lon": 78.4500, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Balanagar Industrial East", "lat": 17.4700, "lon": 78.4600, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "Alwal South Side", "lat": 17.5000, "lon": 78.5050, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Shamirpet South", "lat": 17.6000, "lon": 78.5150, "operator": "Relay Charge", "capacity": "100kW DC"},
    {"name": "Medchal East Road", "lat": 17.6300, "lon": 78.5000, "operator": "Go-E", "capacity": "15kW AC"},
   
   
    {"name": "Gundlapochampally North", "lat": 17.5550, "lon": 78.4550, "operator": "Relay Charge", "capacity": "15kW AC"},
    {"name": "Kompally Residential", "lat": 17.5620, "lon": 78.4750, "operator": "Go-E", "capacity": "50kW DC"},
    {"name": "Medchal Highway South", "lat": 17.6100, "lon": 78.4900, "operator": "Tata Power", "capacity": "120kW DC"},
    {"name": "Kandlakoya Road East", "lat": 17.5900, "lon": 78.4750, "operator": "ChargeZone", "capacity": "25kW AC"},
    {"name": "ORR Exit 7 Access", "lat": 17.5750, "lon": 78.5000, "operator": "Ather", "capacity": "50kW DC"},
    {"name": "Gateway Medchal North", "lat": 17.6420, "lon": 78.4650, "operator": "Relay Charge", "capacity": "100kW DC"},
]

# Append the new stations to the core list
HYDERABAD_STATIONS.extend(KANDLAKOYA_MEDCHAL_STATIONS)
HYDERABAD_STATIONS.extend(FULL_HYDERABAD_COVERAGE)




# --- Static Data function (replaces API call) ---
def fetch_local_stations(lat, lon, max_distance_km):
    """
    Filters the static list of Hyderabad stations to show only those within max_distance_km.
    """
    nearby_stations = []
    user_coords = (lat, lon)
    
    for station in HYDERABAD_STATIONS:
        station_coords = (station["lat"], station["lon"])
        distance_km = geodesic(user_coords, station_coords).km
        
        if distance_km <= max_distance_km:
            # Add the distance to the station dictionary before returning
            station['distance_km'] = distance_km 
            nearby_stations.append(station)
            
    return nearby_stations


# FIXED: Set timeout directly on the geolocator instance, removing the problematic import
geolocator = Nominatim(user_agent="ev_station_finder", timeout=5)

# CHANGED: Set the maximum distance (in kilometers) to search and filter stations to 10.0 km
NEARBY_RADIUS_KM = 10.0 


def home_page(current_user):
    # --- Check for Map Click and Overwrite Location ---
    # This entire block uses 'map_clicked_lat' and 'map_clicked_lon'
    if 'map_clicked_lat' in st.session_state and 'map_clicked_lon' in st.session_state:
        st.session_state['user_lat_override'] = st.session_state.map_clicked_lat
        st.session_state['user_lon_override'] = st.session_state.map_clicked_lon 
        st.session_state['location_source'] = "Map Clicked"
        del st.session_state['map_clicked_lat']
        del st.session_state['map_clicked_lon']
        st.rerun()
        
    # --- Glassmorphic Theme CSS (Unchanged) ---
    st.markdown(
        """
        <style>
        /* Whole App */
        .stApp {
            background: radial-gradient(circle at top left, rgb(117, 210, 202), rgba(95, 113, 111, 0.85), rgb(76, 95, 100));
        }

        /* Main Content Area Styling */
        .main .block-container {
            background: rgba(40, 40, 40, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(144, 238, 144, 0.4);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(144, 238, 144, 0.3);
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6, .stSubheader {
            color: #bfffc8;
            text-shadow: 0px 0px 8px rgba(144, 238, 144, 0.8);
        }
        h1 { text-align: left; }

        /* Input Widgets (text, number, selectbox) */
        .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div {
            border: 2px solid rgba(144, 238, 144, 0.6) !important;
            border-radius: 10px;
            background: rgba(42, 42, 42, 0.8) !important;
            color: #f1f1f1 !important;
            font-weight: 500;
        }
        label { color: #a8ffb0 !important; font-weight: bold; }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #90ee90, #5cd65c);
            color: #0a0a0a !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }

        /* Alerts */
        .stAlert {
            background: rgba(144, 238, 144, 0.1);
            border-left: 5px solid #90ee90;
            color: #bfffc8;
            border-radius: 10px;
        }
        .stAlert.st-alert-warning {
            background: rgba(255, 165, 0, 0.1);
            border-left: 5px solid #ffa500;
            color: #ffdead;
        }

        /* Folium Map Container */
        .stFoliumMap { border-radius: 15px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Layout for Title and Logout Button (Unchanged) ---
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title("⚡ EV Charging Dashboard")
    with col2:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            if 'email' in st.session_state:
                del st.session_state['email']
            st.rerun()

    # --- Vehicle selection from user's data (Unchanged) ---
    user_data = st.session_state.users.get(current_user, {})
    user_vehicles = user_data.get("vehicles", []) 
    if not user_vehicles:
        st.warning("⚠️ No vehicles found for your account.")
        st.stop()
    selected_vehicle = st.selectbox("Choose your vehicle:", user_vehicles)
    st.success(f"Dashboard loaded for vehicle: **{selected_vehicle}**")

    # --- Location Inputs and Detection ---
    
    st.subheader("1. Find Your Location")
    
    if 'search_loc_input' not in st.session_state:
        st.session_state.search_loc_input = ""
    if 'user_lat_override' not in st.session_state:
        st.session_state.user_lat_override = None
    if 'user_lon_override' not in st.session_state:
        st.session_state.user_lon_override = None
    if 'location_source' not in st.session_state:
        st.session_state.location_source = "Initial"


    search_location = st.text_input("Search for a new location (e.g., 'Kondapur, Hyderabad')", 
                                    value=st.session_state.search_loc_input,
                                    key="search_loc")
    st.session_state.search_loc_input = search_location
    
    user_lat = None
    user_lon = None
    location_source = "Unknown Location"
    
    
    # PRIORITY 1: Map Click or Manual Lat/Lon Override
    if st.session_state.user_lat_override is not None:
        user_lat = st.session_state.user_lat_override
        user_lon = st.session_state.user_lon_override
        location_source = st.session_state.location_source
        st.info(f"📍 Location set by: {location_source}")
    
    # PRIORITY 2: Search Input
    if search_location:
        try:
            with st.spinner(f"Searching for '{search_location}'..."):
                loc = geolocator.geocode(search_location)
            if loc:
                user_lat = loc.latitude
                user_lon = loc.longitude
                location_source = f"Searched: {loc.address}"
                st.info(f"📍 Location set to: {loc.address}")
                st.session_state.user_lat_override = user_lat
                st.session_state.user_lon_override = user_lon
            else:
                st.warning("Could not find coordinates for your search term. Using previous location.")
                
        except Exception:
            st.error("Error connecting to location service.")

    # PRIORITY 3: Auto-detection (only runs if no search/override has been set)
    elif user_lat is None:
        location = get_geolocation()
        if location:
            user_lat = location["coords"]["latitude"]
            user_lon = location["coords"]["longitude"]
            location_source = "Auto-detected"
            st.info(f"✅ Your location detected automatically: Latitude {user_lat:.4f}, Longitude {user_lon:.4f}")
        else:
            st.warning("Cannot get your location automatically. Please use the search bar above.")

    # If all detection methods fail, fall back to a default location
    if user_lat is None:
        user_lat = 17.44  # Hyderabad center
        user_lon = 78.34
        location_source = "Default Hyderabad"
        st.warning("Using default location. Please use the search bar to set your location.")

    
    user_coords = (user_lat, user_lon)
    
    # --- Live Station Discovery (Now using static data) ---
    st.subheader(f"2. Live Charging Stations (within {NEARBY_RADIUS_KM} km)")
    
    with st.spinner(f"Searching for stations near {location_source}..."):
        # Use the static function instead of the unreliable API call
        stations_with_distance = fetch_local_stations(user_lat, user_lon, NEARBY_RADIUS_KM)

    if not stations_with_distance:
        st.error(f"😔 No charging stations found within {NEARBY_RADIUS_KM} km of this location.")
        stations_to_plot = []
        map_zoom = 10
    else:
        # The fetch_local_stations function already calculated distance_km
        stations_to_plot = sorted(stations_with_distance, key=lambda x: x['distance_km'])
        
        st.info(f"🔌 Found {len(stations_to_plot)} simulated charging stations.")
        
        # Calculate max distance from the actual filtered list for better zoom
        max_distance = max(s['distance_km'] for s in stations_to_plot) if stations_to_plot else 5
        map_zoom = 14 if max_distance < 5 else 12 
        
    
    # --- Folium Map Initialization (Centered on User) ---
    m = folium.Map(location=[user_lat, user_lon], zoom_start=map_zoom) 

    folium.Marker(
        [user_lat, user_lon], 
        popup=f"You are here 🚗<br>({location_source})",
        icon=folium.Icon(color="blue", icon="user", prefix="fa")
    ).add_to(m)

    marker_cluster = MarkerCluster().add_to(m)

    for s in stations_to_plot:
        distance_display = f"{s['distance_km']:.2f} km"
        
        popup_html = f"""
        <b>{s['name']}</b><br>
        Operator: {s.get('operator', 'N/A')}<br>
        Capacity: {s.get('capacity', 'N/A')}<br>
        Distance: {distance_display}<br>
        <hr style='margin: 5px 0;'>
        <i style='cursor:pointer;'>Click to book slot</i>
        """
        
        folium.Marker(
            location=[s["lat"], s["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="green", icon="bolt", prefix="fa")
        ).add_to(marker_cluster)

    map_data = st_folium(m, width=700, height=500)

    # --- Click-to-Search (Map Click) Logic ---
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]

        st.session_state['map_clicked_lat'] = clicked_lat
        st.session_state['map_clicked_lon'] = clicked_lon
        st.session_state['location_source'] = "Map Clicked"

        st.rerun()

    # --- Click-to-book logic ---
    if map_data and map_data.get("last_object_clicked_popup"):
        clicked_popup_html = map_data["last_object_clicked_popup"]
        selected_station_name = None
        
        for s in stations_to_plot:
            if s["name"] in clicked_popup_html:
                selected_station_name = s["name"]
                break
        
        if selected_station_name:
            st.session_state["selected_vehicle"] = selected_vehicle
            st.session_state["selected_station"] = selected_station_name
            st.session_state["page"] = "book"
            st.rerun()
