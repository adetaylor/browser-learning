# Solutions

Example solutions (there may be others!)

# Exercise 4b

```
text = ""
num = random.randrange(0, 12)
for x in range(0, num):
    text += random.choice(["<tr>", "</tr>", "</td>", "<td>", "<table>", "</table>", "hello", "<th>", "</th>"])
return text
```

This should quite quickly generate:

```
<table>
<th>
some-data
```

which will cause a crash in the absence of a `<tr>` or `<td>`
