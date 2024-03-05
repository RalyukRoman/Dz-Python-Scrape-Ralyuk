# print(response.text)
#
# with open('quotes.html', 'w', encoding='utf-8') as file:
#     file.write(response.text)
#
# with open('quotes.html', 'r') as file:
#     html = file.read()
a = r'<Selector query="descendant-or-self::*[(@class and contains(concat(' ', normalize-space(@class), ' '), ' instock ')) and (@class and contains(concat(' ', normalize-space(@class), ' '), ' availability '))]/*" data='<i class="icon-ok"></i>'>'
print(a)