import os
import pandas as pd

configfile: "config.json"
GLOBAL_REF_PATH = config["globalResources"]
GLOBAL_TMPD_PATH = config["globalTmpdPath"]

os.makedirs(GLOBAL_TMPD_PATH, exist_ok=True)

##### BioRoot utilities #####
module BR:
    snakefile: github("BioIT-CEITEC/bioroots_utilities", path="bioroots_utilities.smk",branch="master")
    config: config

use rule * from BR as other_*

config = BR.load_organism()


##### Config processing #####
sample_tab_initial = pd.DataFrame.from_dict(config["samples"],orient="index")
sample_tab = pd.DataFrame({"sample_name" : [],"sample_name_mother" : [],"sample_name_father" : [],"sample_name_offspring" : []})
sample_tab["sample_name"]=sample_tab_initial["donor"].unique()
for index, row in sample_tab.iterrows():
    sample_tab.loc[index,"sample_name_mother"] = sample_tab_initial.loc[(sample_tab_initial["donor"]==row["sample_name"]) & (sample_tab_initial["origin_id"]=="mother"),"sample_name"].to_string(index=False)
    sample_tab.loc[index,"sample_name_father"] = sample_tab_initial.loc[(sample_tab_initial["donor"]==row["sample_name"]) & (sample_tab_initial["origin_id"]=="father"),"sample_name"].to_string(index=False)
    sample_tab.loc[index,"sample_name_offspring"] = sample_tab_initial.loc[(sample_tab_initial["donor"]==row["sample_name"]) & (sample_tab_initial["origin_id"]=="offspring"),"sample_name"].to_string(index=False)


all_samples = sample_tab_initial["sample_name"].dropna().unique().tolist()
all_donors  = sample_tab_initial["donor"].dropna().unique().tolist()         

wildcard_constraints:
    sample = "|".join(all_samples),
    sample_name = "|".join(all_donors)
####################################
# RULE ALL
rule all:
    input:
       final_variants = expand("genomic_varcalls/{sample_name}_phased.vcf.gz", sample_name = sample_tab.sample_name)

include: "rules/triophaser.smk"
