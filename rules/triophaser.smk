rule haplotypecaller:
    input:
        bam = "mapped/{sample}.bam",
        fasta = config["organism_fasta"]
    output:
        vcf = "genomic_varcalls/{sample}.vcf.gz"
    log: "logs/haplotypecaller/{sample}.log"
    threads: 8
    conda: "../wrappers/gatk/env.yaml"
    wrapper: "../wrappers/gatk/script.py"

rule trioPhaser:
    input:
        mother = expand("genomic_varcalls/{mother_vcf}.vcf.gz", mother_vcf = sample_tab.loc[sample_tab.sample_name == wildcards.sample_name, "sample_name_mother"])[0],
        father = expand("genomic_varcalls/{father_vcf}.vcf.gz", father_vcf = sample_tab.loc[sample_tab.sample_name == wildcards.sample_name, "sample_name_father"])[0],
        offspring = expand("genomic_varcalls/{offspring_vcf}.vcf.gz", offspring_vcf = sample_tab.loc[sample_tab.sample_name == wildcards.sample_name, "sample_name_offspring"])[0]
    output:
        vcf = "genomic_varcalls/{sample_name}_phased.vcf.gz"
    log: "logs/trioPhaser/{sample_name}.log"
    threads: 10
    params:
        call_quality = config["call_quality"]
    conda: "../wrappers/triophaser/env.yaml"
    wrapper: "../wrappers/triophaser/script.py"