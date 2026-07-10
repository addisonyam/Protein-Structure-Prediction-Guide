import json
import numpy as np
import pandas as pd 

# ============================ 
# 1. Load confidence file 
# ============================ 
with open("ay005_confidences.json") as f: 
    data = json.load(f) 

# ============================ 
# 2. Overall pLDDT 
# ============================ 
plddt = np.array(data["atom_plddts"]) 

print("Number of atoms:", len(plddt)) 
print("First 10 atom pLDDTs:") 
print(plddt[:10]) 

print("Mean pLDDT:", plddt.mean()) 
print("") 

# ============================
# 3. Chain-level pLDDT 
# ============================
df = pd.DataFrame({ 
    "chain": data["atom_chain_ids"], 
    "plddt": data["atom_plddts"] 
}) 

print("Mean pLDDT by chain:") 
print(df.groupby("chain").mean()) 
print("") 

# ============================ 
# 4. PAE analysis 
# ============================
pae = np.array(data["pae"]) 

print("PAE matrix shape:", pae.shape) 
print("") 

# AY005:
# helix: residues 1-35 
# linker: residues 36-41 
# domain: residues 42-248 

helix_domain = pae[0:35, 41:248] 
linker_domain = pae[35:41, 41:248] 
helix_linker = pae[0:35, 35:41] 

print("Helix-domain PAE:", 
      helix_domain.mean()) 
print("Linker-domain PAE:", 
      linker_domain.mean()) 
print("Helix-linker PAE:", 
      helix_linker.mean()) 
print("") 

# ============================ 
# 5. Trimer chain PAE 
# ============================ 
chainA = slice(0,248) 
chainB = slice(248,496) 
chainC = slice(496,744) 

AB = pae[chainA, chainB]
BC = pae[chainB, chainC]
AC = pae[chainA, chainC] 

print("A-B PAE:", AB.mean()) 
print("B-C PAE:", BC.mean()) 
print("A-C PAE:", AC.mean()) 
print("") 

# ============================ 
# 6. ipTM / ranking score 
# ============================ 
with open("ay005_summary_confidences.json") as f: 
    summary = json.load(f) 
print("Summary confidence keys:") 
print(summary.keys()) 
print("") 

# Try common AF3 names 
for key in ["iptm", "ipTM", "iptm_score", "interface_ptm"]: 
    if key in summary: 
        print("ipTM:", summary[key]) 
        break 

else: 
    print("ipTM not found. Available values:") 
    print(summary) 
