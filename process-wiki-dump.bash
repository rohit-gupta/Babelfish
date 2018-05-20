cat hiwiki-20180501-langlinks.sql | grep -n ",'en'," | cut -c-10 | awk -F ":" '{print $1}' > hi-en_link_rows.txt
awk 'NR==FNR{a[$1]++;next} { if(FNR in a){ print } }' hi-en_link_rows.txt hiwiki-20180501-langlinks.sql > links_raw_queries.txt

grep -n "INSERT INTO" hiwiki-20180501-page.sql | cut -c-80 | awk -F ":" '{print $1}' > page_id_titles_lines.txt
awk 'NR==FNR{a[$1]++;next} { if(FNR in a){ print } }' page_id_titles_lines.txt hiwiki-20180501-page.sql > pages_raw_queries.txt

python parse_id_titles.py > parsed_page_titles.tsv
