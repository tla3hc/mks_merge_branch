import re

def extract_development_paths(text):
    # Find the section after "Development Paths:" 
    match = re.search(r'Development Paths:(.*?)(?=\n\S|$)', text, re.DOTALL)
    
    if match:
        # Extract lines starting with a tab
        paths_section = match.group(1)
        dev_paths = re.findall(r'^\s+(.*?)(?=\s|$)', paths_section, re.MULTILINE)
        return dev_paths
    else:
        return []

# Example usage with your provided text
cli_output = '''
Project Name: /SWC_USS/01_PROD/30_CG/project.pj
Repository Location: /SWC_USS/01_PROD/30_CG/project.pj
Server: mksprod.in.audi.vwg:7001
Configuration Path: #/SWC_USS#01_PROD/30_CG
Restricted: false
Last Checkpoint: 1.27
Last Checkpoint Date: Aug 22, 2024 10:14:18 PM
Change Package:
    No Change Package Information Available
Members: 1
Subprojects: 23
Description:
Attributes: none
Development Paths:
    DP_MOD_USS_0101_1200_0000 (1.3)
    DP_USS_INT2.0_0201-1201-0000_MOD (1.4)
    DP_USS_INT3.0_0302-1202-0100_BOSCH (1.5)
    DP_USS_INT3.0_0302-1202-0100_TTTech (1.6)
    DP_USS_INT3.0_0302-1202-0200_TTTech (1.7)
    DP_USS_INT3.0_0302-1202-0200_BOSCH (1.7.1.6)
    DP_MOD_USS_INT3.2_0404-1200-0000 (1.9)
    DP_FE_USS_INT4.2_0505_0000_0000 (1.10)
    DP_FE_USS_INT4.3_0605_0000_0000 (1.11)
    DP_MOD_USS_C02_INT3.2 (1.11.1.3)
    DP_FE_USS_C03_0706_0000_0000 (1.12)
    DP_CG_USS_C03_0806-0000-0000 (1.12.1.7)
    CG_USS_C05_0907_0000_0000 (1.13)
    DP_CG_USS_C05_0907_0000_0000 (1.13)
    DP_MOD_USS_C05inC03 (1.13)
    DP_USS_C05_0907_0001_0000 (1.14)
    DP_USS_C05_1007_0000_0000 (1.16)
    DP_USS_C05_1107_0000_0000 (1.17)
    DP_USS_C07_CG_Preparation (1.17.1.2)
    DP_USS_C05_1107_0000_0000_TC_updated (1.17.1.4)
    CG_USS_C05_1207_0000_0000 (1.18)
    DP_USS_C07_1038_0000_0000 (1.20)
    DP_USS_C08_1409_0000_0000 (1.21)
    DP_MOD_USS_C08inC05 (1.21)
    DP_CG_USS_C08_1509_0000_0000 (1.22)
    DP_CG_USS_C08_1609_0000_0000 (1.23)
    DP_CG_USS_C0A_1609_0000_0000 (1.24)
    DP_CG_USS_C08_1710_0000_0000 (1.26)
    DP_CG_USS_C08_1710_0000_0000_V01 (1.27)
    DP_FE_USS_C08_S912inS801 (1.23.1.6)
Associated Issues: none
'''

paths = extract_development_paths(cli_output)
for path in paths:
    print(path)
