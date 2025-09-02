######################################
# wrapper for rule: trioPhaser
######################################
import os
import subprocess
from snakemake.shell import shell

log_filename = str(snakemake.log)

f = open(log_filename, 'wt')
f.write("\n##\n## wrapper: genomic gatk \n##\n")
f.close()

shell.executable("/bin/bash")

version = str(subprocess.Popen("conda list ", shell=True, stdout=subprocess.PIPE).communicate()[0], 'utf-8')
f = open(log_filename, 'at')
f.write("## CONDA: "+version+"\n")
f.close()

if str(snakemake.params.assembly) == "GRCh37":
    build_version = "37"
elif str(snakemake.params.assembly) == "GRCh38":
    build_version = "38"
else:
    error_msg = f"Error: Unsupported assembly '{str(snakemake.params.assembly)}'. Only GRCh37 and GRCh38 assemblies are supported."
    f = open(log_filename, 'at')
    f.write("## ERROR: " + error_msg + "\n")
    f.close()
    raise ValueError(error_msg)

command = "python3 " + os.path.abspath(os.path.dirname(__file__)) + "/trio_phaser.py" + \
          " -c " + str(snakemake.input.offspring) + \
          " -p " + str(snakemake.input.father) + \
          " -m " + str(snakemake.input.mother) + \
          " -o " + str(snakemake.output.vcf) + \
          " --number_of_tasks " + str(snakemake.threads) + \
          " --build_version " + build_version + \
          " --call_quality " + str(snakemake.params.call_quality) + \
          " -r haplotyping_references >> " + log_filename + " 2>&1"

f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)