import os
from rdkit import Chem
import subprocess

# User input
input_sdf = "molecules.sdf"
output_dir = "pdbqt_output"
failed_log = "failed_smiles.txt"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Prepare log file
with open(failed_log, 'w') as fail_log:
    suppl = Chem.SDMolSupplier(input_sdf)
    for i, mol in enumerate(suppl):
        if mol is None:
            fail_log.write(f"Molecule {i} - RDKit could not parse.\n")
            continue

        try:
            smiles = Chem.MolToSmiles(mol)
        except:
            fail_log.write(f"Molecule {i} - SMILES conversion failed.\n")
            continue

        # Write temporary SDF for this molecule
        mol_filename = os.path.join(output_dir, f"mol_{i}.sdf")
        writer = Chem.SDWriter(mol_filename)
        writer.write(mol)
        writer.close()

        # Convert SDF to PDBQT using Open Babel
        pdbqt_filename = os.path.join(output_dir, f"mol_{i}.pdbqt")
        try:
            result = subprocess.run(
                ['obabel', mol_filename, '-O', pdbqt_filename, '--gen3d'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if not os.path.isfile(pdbqt_filename) or os.path.getsize(pdbqt_filename) == 0:
                fail_log.write(f"{smiles}\n")  # Write SMILES to failed list
                print(f"[FAIL] Molecule {i}: PDBQT not generated")
            else:
                print(f"[OK] Molecule {i} converted to PDBQT")
        except Exception as e:
            fail_log.write(f"{smiles}\n")
            print(f"[ERROR] Molecule {i}: {e}")

        # Optionally delete intermediate SDFs:
        os.remove(mol_filename)
