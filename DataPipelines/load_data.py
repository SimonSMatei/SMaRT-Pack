from pathlib import Path
from SMaRT_Pack import load_aflow_data

### Main Parameters ###

lattice_parameter_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),natoms(*),volume_cell(*),$paging(1,1000)'
lattice_parameter_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),natoms(*),volume_cell(*),$paging(1,1000)'

thermal_conductivity_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_thermal_conductivity_300K(*),$paging(1,1000)'
thermal_conductivity_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_thermal_conductivity_300K(*),$paging(1,1000)'

coef_thermal_expansion_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_thermal_expansion_300K(*),$paging(1,1000)'
coef_thermal_expansion_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_thermal_expansion_300K(*),$paging(1,1000)'

### Electronic Properties ###

band_gap_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),Egap(*),$paging(1,1000)'
band_gap_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),Egap(*),$paging(1,1000)'

### Magnetic Properties ###

atom_magnetic_moment_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),spinD(*),$paging(1,1000)'
atom_magnetic_moment_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),spinD(*),$paging(1,1000)'

### Mechanical Properties ###

mechanical_properties_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),ael_bulk_modulus_vrh(*),ael_poisson_ratio(*),ael_shear_modulus_vrh(*),ael_youngs_modulus_vrh(*),$paging(1,1000)'
mechanical_properties_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),ael_bulk_modulus_vrh(*),ael_poisson_ratio(*),ael_shear_modulus_vrh(*),ael_youngs_modulus_vrh(*),$paging(1,1000)'

### Thermodynamic Properties ###

debye_temperature_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_debye(*),$paging(1,1000)'
debye_temperature_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),agl_debye(*),$paging(1,1000)'

formation_enthalpy_icsd_url = 'https://aflowlib.org/API/aflux/?species(C),$catalog(ICSD),spacegroup_relax(225),Pearson_symbol_relax(cF8),enthalpy_formation_atom(*),$paging(1,1000)'
formation_enthalpy_aflow_url = 'https://aflowlib.org/API/aflux/?species(C),spacegroup_relax(225),Pearson_symbol_relax(cF8),enthalpy_formation_atom(*),$paging(1,1000)'


if __name__ == '__main__':

    parameters = [lattice_parameter_icsd_url, lattice_parameter_aflow_url, thermal_conductivity_icsd_url, 
                  thermal_conductivity_aflow_url, coef_thermal_expansion_icsd_url, coef_thermal_expansion_aflow_url, 
                  band_gap_icsd_url, band_gap_aflow_url, atom_magnetic_moment_icsd_url, atom_magnetic_moment_aflow_url, 
                  mechanical_properties_icsd_url, mechanical_properties_aflow_url, debye_temperature_icsd_url, 
                  debye_temperature_aflow_url, formation_enthalpy_icsd_url, formation_enthalpy_aflow_url]

    file_names = ['lattice_parameter_icsd.csv', 'lattice_parameter_aflow.csv', 'thermal_conductivity_icsd.csv', 
                  'thermal_conductivity_aflow.csv', 'coef_thermal_expansion_icsd.csv', 'coef_thermal_expansion_aflow.csv', 
                  'band_gap_icsd.csv', 'band_gap_aflow.csv', 'atom_magnetic_moment_icsd.csv', 'atom_magnetic_moment_aflow.csv', 
                  'mechanical_properties_icsd.csv', 'mechanical_properties_aflow.csv', 'debye_temperature_icsd.csv', 
                  'debye_temperature_aflow.csv', 'formation_enthalpy_icsd.csv', 'formation_enthalpy_aflow.csv']



    for p, f in zip(parameters, file_names):
        if 'icsd' in f:
            load_aflow_data(p, save_csv = True, csv_path = Path(__file__).resolve().parent.parent / 'DataBases' / 'RawData' / 'ICSDCarbides' / f)
        else:
            load_aflow_data(p, save_csv = True, csv_path = Path(__file__).resolve().parent.parent / 'DataBases' / 'RawData' / 'AllAFLOWCarbides' / f)