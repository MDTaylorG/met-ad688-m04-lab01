import json

with open('lab06_mariatg.ipynb', 'r') as f:
    nb = json.load(f)

# Fix cell 7 - move col import to top
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'from pyspark.sql.functions import explode' in source:
            cell['source'] = [
                "from pyspark.sql.functions import explode, split, trim, col, count\n",
                "df_skills = df.select('NAICS2_NAME', explode(split(df.SKILLS_NAME, ',')).alias('skill')).withColumn('skill', trim(col('skill'))).filter(col('skill') != '')\n",
                "df_skills_top = df_skills.groupBy('NAICS2_NAME', 'skill').agg(count('*').alias('skill_count')).orderBy('skill_count', ascending=False).limit(50).toPandas()\n",
                "fig6 = px.bar(df_skills_top, x='NAICS2_NAME', y='skill_count', color='skill', title='Skill Demand by Industry', template='plotly_white', labels={'NAICS2_NAME': 'Industry', 'skill_count': 'Skill Count'})\n",
                "fig6.update_layout(title_font_size=20, xaxis_tickangle=-45)\n",
                "fig6.write_image('_output/skill_demand.png')\n",
                "fig6.show()\n",
                "print('Technology and professional services industries demand the most diverse skill sets. SQL, Python, and communication skills appear consistently across multiple industries.')\n"
            ]

with open('lab06_mariatg.ipynb', 'w') as f:
    json.dump(nb, f)

print("Fixed!")
