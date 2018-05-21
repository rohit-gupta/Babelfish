

# Extract Hindi Article Text
python WikiExtractor.py -o parsed-wiki-articles-json --templates hi-templates.tpl --json --discard_elements gallery,timeline,noinclude  --filter_disambig_pages ../hiwiki-20180501-pages-articles.xml.bz2              


# Get link information from SQL Dump
cat hiwiki-20180501-langlinks.sql | grep -n ",'en'," | cut -c-10 | awk -F ":" '{print $1}' > hi-en_link_rows.txt
awk 'NR==FNR{a[$1]++;next} { if(FNR in a){ print } }' hi-en_link_rows.txt hiwiki-20180501-langlinks.sql > links_raw_queries.txt


# Get Hindi page title information from SQL Dump
grep -n "INSERT INTO" hiwiki-20180501-page.sql | cut -c-80 | awk -F ":" '{print $1}' > page_id_titles_lines.txt
awk 'NR==FNR{a[$1]++;next} { if(FNR in a){ print } }' page_id_titles_lines.txt hiwiki-20180501-page.sql > pages_raw_queries.txt

# Parse Page title dump and Links dump
python parse_id_titles.py > parsed_page_titles.tsv
python parse_links.py > parsed_links.tsv

# Cross reference Link and Title information to match article titles 
python match_titles.py


