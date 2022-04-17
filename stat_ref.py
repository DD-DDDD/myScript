import re

ref_file = open('my.bin', 'r', encoding='utf8')

ref_lines = ref_file.readlines()
year_list = {}

conference = []
journal = []
other = []

article_type_re = re.compile(r'\[[JCR]\]')
year_re = re.compile(r'\d+\,|\d+\:|\d+\.')
for line in ref_lines:
    article_type = article_type_re.findall(line.strip())[0]

    if article_type == '[J]':
        journal.append(line)
    elif article_type == '[C]':
        conference.append(line)
    else:
        other.append(line)

    year = year_re.findall(line.strip())[0][:4]
    year_list[year] = year_list.get(year, 0) + 1

# 期刊文章总数
print(f'journal size: {len(journal)}')
# 会议文章总数
print(f'conference size: {len(conference)}')
# 其他文章数
print(f'other size: {len(other)}')
# 参考文献总数
all_size = len(journal) + len(conference) + len(other)
print(f'all size: {all_size}')
# 近5年文章占比
# 近3年文章占比
top5 = 0
top3 = 0
five_year = ['2021', '2020', '2019', '2018', '2017']

for key in year_list.keys():
    if key in five_year:
        top5 += year_list[key]
    if key in five_year[:3]:
        top3 += year_list[key]

print(f'top 5 year: {round((top5 / all_size) * 100, 2)}%')
print(f'top 3 year: {round((top3 / all_size) * 100, 2)}%')

