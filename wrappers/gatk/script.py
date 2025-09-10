######################################
# wrapper for rule: genomic_gatk
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

command = "gatk --java-options -Xmx8g HaplotypeCaller -R " + str(snakemake.input.fasta) + \
          " -I " + snakemake.input.bam + \
          " -O " + snakemake.output.vcf + \
          " -ERC GVCF >> " + log_filename + " 2>&1"

f = open(log_filename, 'at')
f.write("## COMMAND: "+command+"\n")
f.close()
shell(command)

command = "zcat " + snakemake.output.vcf + " | sed -E 's/^([0-9XY]+|MT)\\t/chr\\1\\t/; s/(ID=)([0-9XY]+|MT)([>,])/\\1chr\\2\\3/; s/chrMT/chrM/' | bgzip > " + str(snakemake.output.vcf).replace(".vcf.gz", "_tmp.vcf.gz") + " 2>> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("##COMMAND:"+command+"\n")
f.close()
shell(command)

command = "mv " + str(snakemake.output.vcf).replace(".vcf.gz", "_tmp.vcf.gz") + " " + snakemake.output.vcf + " >> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("##COMMAND:"+command+"\n")
f.close()
shell(command)

command = "tabix -p vcf " + snakemake.output.vcf + " >> " + log_filename + " 2>&1"
f = open(log_filename, 'at')
f.write("##COMMAND:"+command+"\n")
f.close()
shell(command)